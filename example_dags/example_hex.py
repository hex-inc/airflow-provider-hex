from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow_provider_hex.operators.hex import HexRunProjectOperator

PROJ_ID = "76dec7ff-c1cc-4949-8406-05e574f22353"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("hex", max_active_runs=1, default_args=default_args)

sync_run = HexRunProjectOperator(
    task_id="sync_run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
)

async_run = HexRunProjectOperator(
    task_id="async_run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
    synchronous=False
)
