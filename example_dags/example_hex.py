from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow_provider_hex.operators.hex import HexRunProjectOperator

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

sync = HexRunProjectOperator(
    task_id="run",
    hex_conn_id="hex_default",
    project_id="391a12e6-8085-4781-bfed-e6cffc2c8346",
    dag=dag,
)
