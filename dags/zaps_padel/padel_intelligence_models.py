import os

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.utils.dates import days_ago
from zaps_core.utils.airflow_notifications_utils import \
    errors_notification_telegram
from zaps_core.utils.dbt_utils import build_dbt_command

# Carga la variable airflow home path
airflow_home_path = os.getenv('AIRFLOW_HOME')
dbt_dir = f'{airflow_home_path}/dbt/{Variable.get("ZAPS_PADEL_DBT_PROFILE")}'


@dag(
    dag_id='padel_pi_models',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    concurrency=6,
    max_active_runs=1,
    tags=['padel', 'intelligence', 'dbt']
)
def padel_pi_models():
    # Tarea para ejecutar dbt test
    @task.bash(on_failure_callback=errors_notification_telegram)
    def run_pi_models():
        dbt_kwargs = {
            'project-dir': dbt_dir,
            'profiles-dir': dbt_dir,
            'profile': Variable.get('ZAPS_PADEL_DBT_PROFILE')
        }
        return build_dbt_command(
            'run',
            **dbt_kwargs
        )
    run_pi_models()


padel_pi_models = padel_pi_models()
