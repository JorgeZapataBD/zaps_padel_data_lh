from typing import Literal

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram

from plugins.zaps_padel.operators.padel_common import \
    operator_create_external_table
from plugins.zaps_padel.operators.padel_intelligence import (
    operator_pi_get_match_list2gcs, operator_pi_get_match_stats2gcs)

# Categories to download
l_stats_types = ['sets', 'player', 'team', 'lastpoints', None]


@dag(
    dag_id='padel_intelligence_matches_stats',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=['padel', 'intelligence', 'matches']
)
def padel_intelligence_matches():
    @task.branch(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def get_matches_list2gcs():
        """
        Task which get list of public matchs of Paddel Intelligence Web. Actually get token is manually.
        This part need an update for get automatically the credentials.
        """
        b_is_new_data = operator_pi_get_match_list2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_padel_intelligence_matches'
        )
        return 'matches_stats' if b_is_new_data else 'not_data'

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def create_match_list_bq_table():
        """
        Task which create external table if not exists
        """
        operator_create_external_table(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_padel_intelligence_matches',
            gcs_prefix='matches_list',
            bq_dataset_id='raw',
            bq_table_id='raw_pi_matches_list'
        )

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def get_matches_stats2gcs(stats_type: Literal['sets', 'player', 'team', 'lastpoints'] | None):
        """
        Task which get stats of each public match based on type of Stats.
        """
        operator_pi_get_match_stats2gcs(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_padel_intelligence_matches',
            stats_type=stats_type
        )

    @task(show_return_value_in_logs=False, on_failure_callback=errors_notification_telegram)
    def create_match_stats_bq_table(stats_type: Literal['sets', 'player', 'team', 'lastpoints'] | None):
        """
        Task which create external table if not exists
        """
        operator_create_external_table(
            gcp_project_id=Variable.get('ZAPS_PADEL_GCP_PROJECT_ID'),
            gcp_conn_id='zaps_padel_gcp',
            gcs_bucket='raw_padel_intelligence_matches',
            gcs_prefix=f'matches_stats_{stats_type or "resume"}',
            bq_dataset_id='raw',
            bq_table_id=f'raw_pi_matches_stats_{stats_type or "resume"}'
        )

    dummy_task = EmptyOperator(task_id='not_data')

    with TaskGroup("matches_stats") as matches_stats:
        # Match list table
        create_match_list_bq_table()
        # Process stats data
        for s_stats_type in l_stats_types:
            task_stats2gcs = get_matches_stats2gcs.override(task_id=f'pi_load_match_stats_{s_stats_type or "resume"}')(
                stats_type=s_stats_type
            )
            task_stats_bq_table = create_match_stats_bq_table.override(task_id=f'pi_table_match_stats_{s_stats_type or "resume"}')(
                stats_type=s_stats_type
            )
            task_stats2gcs >> task_stats_bq_table
    get_matches_list2gcs_task = get_matches_list2gcs()
    get_matches_list2gcs_task >> [matches_stats, dummy_task]


padel_intelligence_matches = padel_intelligence_matches()
