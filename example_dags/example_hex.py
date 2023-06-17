from datetime import timedelta
from typing import List

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow_provider_hex.operators.hex import HexRunProjectOperator
from airflow_provider_hex.types import NotificationDetails

PROJ_ID = "391a12e6-8085-4781-bfed-e6cffc2c8346"

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

notifications: List[NotificationDetails] = [
    {
        "type": "SUCCESS",
        "includeSuccessScreenshot": True,
        "slackChannelIds": ["HEX666SQG"],
        "userIds": [],
        "groupIds": [],
    }
]

sync_run = HexRunProjectOperator(
    task_id="sync_run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
    input_parameters={"myParam": 42},
    notifications=notifications,
)

async_run = HexRunProjectOperator(
    task_id="async_run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
    synchronous=False,
    input_parameters={"myParam": 42},
)
