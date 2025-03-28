from typing import Literal

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram

from plugins.zaps_padel.operators.padel_common import \
    operator_create_external_table
from plugins.zaps_padel.operators.padel_ranking_fip import (
    operator_get_ranking_fip_files2gcs,
    operator_parser_ranking_fip_files_gcs2gcs)

# Categories to download
fip_categories = ['Male', 'Female', 'Race-Male', 'Race-Female']


@dag(
    dag_id='padel_ranking_fip_files',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=['padel', 'fip', 'ranking']
)
def padel_ranking_fip_files():
    @task.branch(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def ranking_fip_files2gcs(fip_category: Literal['Male', 'Female', 'Race-Male', 'Race-Female']):
        """
        Task which create process wich connect FIP (Federation Interntation Padel) Ranking Files
        to GCS based on category or ranking type
        """
        b_is_new_data = operator_get_ranking_fip_files2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_ranking_fip_padel',
            fip_category=fip_category
        )
        return f'{fip_category}_ranking_fip_parser_gcs2gcs' if b_is_new_data else f'{fip_category}_not_data'

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def ranking_fip_files_parser(fip_category: Literal['Male', 'Female', 'Race-Male', 'Race-Female'], **context):
        """
        Task which convert PDF files from GCS to Parquet Files and load to parsed GCS Bucket
        """
        if context['run_id'].startswith('manual__'):
            date_prefix = (context['execution_date']).strftime('%Y-%m-%d')
        else:
            date_prefix = (context['data_interval_end']).strftime('%Y-%m-%d')
        operator_parser_ranking_fip_files_gcs2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_src_bucket='raw_ranking_fip_padel',
            gcs_dst_bucket='norm_ranking_fip_padel',
            fip_category=fip_category,
            gcs_prefix=date_prefix,
            pages=5
        )

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def create_ranking_fip_bq_table(fip_category: Literal['Male', 'Female', 'Race-Male', 'Race-Female']):
        """
        Task which create external table if not exists
        """
        operator_create_external_table(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='norm_ranking_fip_padel',
            gcs_prefix=fip_category,
            bq_dataset_id='raw',
            bq_table_id=f'raw_ranking_fip_{fip_category.lower().replace("-","_")}'
        )

    for fip_category in fip_categories:
        task_file2gcs = ranking_fip_files2gcs.override(task_id=f'{fip_category}_ranking_fip_files2gcs')(
            fip_category=fip_category
        )
        task_parsefile = ranking_fip_files_parser.override(task_id=f'{fip_category}_ranking_fip_parser_gcs2gcs')(
            fip_category=fip_category
        )
        task_create_table = create_ranking_fip_bq_table.override(task_id=f'{fip_category}_ranking_fip_bq_table')(
            fip_category=fip_category
        )
        dummy_task = EmptyOperator(task_id=f"{fip_category}_not_data")
        task_file2gcs >> [task_parsefile, dummy_task]
        task_parsefile >> task_create_table


padel_ranking_fip_files = padel_ranking_fip_files()
