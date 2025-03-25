from typing import Literal

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram

from plugins.zaps_padel.operators.padel_fip_rankings import (
    operator_get_fip_ranking_files2gcs,
    operator_parser_fip_ranking_files_gcs2gcs)

# Categories to download
fip_categories = ['Male', 'Female', 'Race-Male', 'Race-Female']


@dag(
    dag_id='padel_fip_ranking_files',
    schedule_interval='20 16 * * 6',
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=['padel', 'fip', 'ranking']
)
def padel_fip_ranking_files():
    @task.branch(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def fip_ranking_files2gcs(fip_category: Literal['Male', 'Female', 'Race-Male', 'Race-Female']):
        """
        Task which create process wich connect FIP (Federation Interntation Padel) Ranking Files
        to GCS based on category or ranking type
        """
        b_is_new_data = operator_get_fip_ranking_files2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_ranking_fip_padel',
            fip_category=fip_category
        )
        return f'{fip_category}_fip_ranking_parser' if b_is_new_data else f'{fip_category}_not_data'

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def fip_ranking_files_parser(fip_category: Literal['Male', 'Female', 'Race-Male', 'Race-Female'], **context):
        """
        Task which convert PDF files from GCS to Parquet Files and load to parsed GCS Bucket
        """
        if context['run_id'].startswith('manual__'):
            date_prefix = (context['execution_date']).strftime('%Y-%m-%d')
        else:
            date_prefix = (context['data_interval_end']).strftime('%Y-%m-%d')
        operator_parser_fip_ranking_files_gcs2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_src_bucket='raw_ranking_fip_padel',
            gcs_dst_bucket='norm_ranking_fip_padel',
            fip_category=fip_category,
            gcs_prefix=date_prefix,
            pages=5
        )

    for fip_category in fip_categories:
        task_file2gcs = fip_ranking_files2gcs.override(task_id=f'{fip_category}_fip_ranking_files2gcs')(
            fip_category=fip_category
        )
        task_parsefile = fip_ranking_files_parser.override(task_id=f'{fip_category}_fip_ranking_parser')(
            fip_category=fip_category
        )
        dummy_task = EmptyOperator(task_id=f"{fip_category}_not_data")
        task_file2gcs >> [task_parsefile, dummy_task]


padel_fip_ranking_files = padel_fip_ranking_files()
