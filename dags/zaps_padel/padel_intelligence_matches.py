from typing import Literal

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram

from plugins.zaps_padel.operators.padel_intelligence import (
    operator_pi_get_match_list2gcs, operator_pi_get_match_stats2gcs)

# Categories to download
l_stats_types = ['sets', 'player', 'team', 'lastpoints', None]


@dag(
    dag_id='padel_intelligence_matches_stats',
    schedule_interval='20 16 * * 6',
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

    dummy_task = EmptyOperator(task_id='not_data')

    with TaskGroup("matches_stats") as matches_stats:
        tasks_stats = []
        for s_stats_type in l_stats_types:
            task_stats2gcs = get_matches_stats2gcs.override(task_id=f'padel_intelligence_match_stats_{s_stats_type or "resume"}')(
                stats_type=s_stats_type
            )
            tasks_stats.append(task_stats2gcs)
    get_matches_list2gcs() >> [matches_stats, dummy_task]


padel_intelligence_matches = padel_intelligence_matches()
