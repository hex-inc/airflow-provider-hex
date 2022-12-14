import datetime

import pendulum
import pytest
from airflow import DAG

from airflow_provider_hex.operators.hex import HexRunProjectOperator

TEST_DAG_ID = "my_custom_dag"
DATA_INTERVAL_START = pendulum.datetime(2021, 9, 13, tz="UTC")
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)
TEST_TASK_ID = "my_custom_operator_task"


@pytest.fixture(autouse=True)
def sample_conn(mocker):
    mocker.patch.dict(
        "os.environ",
        AIRFLOW_CONN_HEX_CONN="http://some:password@https%3A%2F%2Fwww.httpbin.org%2F",
    )


@pytest.fixture()
def dag():
    with DAG(
        dag_id=TEST_DAG_ID,
        schedule_interval="@daily",
        start_date=DATA_INTERVAL_START,
    ) as dag:
        HexRunProjectOperator(
            task_id=TEST_TASK_ID,
            hex_conn_id="hex_conn",
            project_id="ABC-123",
            input_parameters={"input_date": "{{ ds }}"},
        )
    return dag


@pytest.fixture()
def fake_dag():
    with DAG(
        dag_id=TEST_DAG_ID,
        schedule="@daily",
        start_date=DATA_INTERVAL_START,
    ) as dag:
        HexRunProjectOperator(
            task_id=TEST_TASK_ID,
            hex_conn_id="hex_conn",
            project_id="ABC-123",
            input_parameters={"input_date": "{{ ds }}"},
        )
    return dag
