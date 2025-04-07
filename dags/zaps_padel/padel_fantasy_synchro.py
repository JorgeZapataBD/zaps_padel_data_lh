import os

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from zaps_core.clients.firestore_client import FirestoreClient
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram
from zaps_core.utils.dbt_utils import build_dbt_command

from plugins.zaps_padel.operators.padel_common import \
    operator_create_external_table
from plugins.zaps_padel.operators.padel_fantasy import (
    operator_padel_fantasy_fromobject2gcs, operator_padel_fantasy_list2gcs)

# List of endpoints to synchro
l_api_endpoints = ['players', 'matches', 'seasons']
# Load airflow variable home path
airflow_home_path = os.getenv('AIRFLOW_HOME')
dbt_dir = f'{airflow_home_path}/dbt/{Variable.get("ZAPS_PADEL_DBT_PROFILE")}'


@dag(
    dag_id='padel_fantasy_synchro',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    concurrency=6,
    max_active_runs=1,
    tags=['padel', 'fantasy', 'lists']
)
def padel_fantasy():

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def get_padel_fantasy_list2gcs(api_endpoint: str):
        """
        Task which load data from padel fantasy API to GCS

        :param api_endpoint: Padel Fantasy API endpoint
        """
        while True:
            # Get parameters from FirestoreClient if exist
            client_fs = FirestoreClient(Variable.get(
                'ZAPS_PADEL_GCP_PROJECT_ID'), 'zaps_padel_gcp')

            d_params = client_fs.get_document(
                collection_name='padel_fantasy',
                doc_id=api_endpoint
            )
            # Creating params request
            if not d_params:
                d_params = {"per_page": 100, 'page': 1, 'ids': []}

            b_new_data = operator_padel_fantasy_list2gcs(
                api_endpoint=api_endpoint,
                api_params=d_params,
                gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
                gcp_conn_id='zaps_padel_gcp',
                gcs_bucket='raw_padel_fantasy',
            )
            if not b_new_data:
                break

    @task.branch(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def get_padel_fantasy_seasons_tournaments2gcs():
        """
        Task which load list of tournaments per season from padel fantasy API to GCS
        """
        # Get parameters from FirestoreClient if exist
        client_fs = FirestoreClient(Variable.get(
            'ZAPS_PADEL_GCP_PROJECT_ID'), 'zaps_padel_gcp')

        d_seasons = client_fs.get_document(
            collection_name='padel_fantasy',
            doc_id='seasons'
        )
        # Create variable data check
        b_is_new_data = False
        if d_seasons:
            d_tournaments = client_fs.get_document(
                collection_name='padel_fantasy',
                doc_id='seasons_tournaments'
            )
            if not d_tournaments:
                l_seasons = d_seasons['ids']
                d_tournaments = {'per_page': 100, 'seasons_ids': [], 'ids': []}
            else:
                l_seasons = [max(d_seasons['ids'])] if sorted(d_seasons['ids']) == sorted(
                    d_tournaments['seasons_ids']) else [x for x in d_seasons['ids'] if x not in d_tournaments['seasons_ids']]

            for s_id in l_seasons:
                d_tournaments['page'] = s_id
                b_tmp_is_new_data = operator_padel_fantasy_fromobject2gcs(
                    api_endpoint='seasons_tournaments',
                    api_params=d_tournaments,
                    gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
                    gcp_conn_id='zaps_padel_gcp',
                    gcs_bucket='raw_padel_fantasy',
                )
                if b_tmp_is_new_data:
                    b_is_new_data = True

            return 'create_tournaments_bq_table' if b_is_new_data else 'not_data'

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def create_tournaments_bq_table():
        """
        Task which create external table if not exists
        """
        operator_create_external_table(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_padel_fantasy',
            gcs_prefix='seasons_tournaments',
            bq_dataset_id='raw',
            bq_table_id='raw_pf_seasons_tournaments'
        )

    @task.bash(on_failure_callback=errors_notification_telegram)
    def run_pf_models():
        """
        Task which execute all staging models of padel fantasy
        """
        dbt_kwargs = {
            'project-dir': dbt_dir,
            'profiles-dir': dbt_dir,
            'profile': Variable.get('ZAPS_PADEL_DBT_PROFILE'),
            'select': ['staging.pf']
        }
        return build_dbt_command(
            'run',
            **dbt_kwargs
        )

    dummy_task = EmptyOperator(task_id='not_data')
    create_tournaments_bq_table_task = create_tournaments_bq_table()
    for api_endpoint in l_api_endpoints:
        task_file2gcs = get_padel_fantasy_list2gcs.override(task_id=f'{api_endpoint}_padelfantasy_files2gcs')(
            api_endpoint=api_endpoint
        )
        if api_endpoint == 'seasons':
            task_file2gcs >> get_padel_fantasy_seasons_tournaments2gcs(
            ) >> [create_tournaments_bq_table_task, dummy_task]
            create_tournaments_bq_table_task >> run_pf_models()
        else:
            task_file2gcs


padel_fantasy = padel_fantasy()
