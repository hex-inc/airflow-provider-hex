import datetime

import pendulum
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunType

DATA_INTERVAL_START = pendulum.now()
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)

TEST_TASK_ID = "my_custom_operator_task"


def test_my_custom_operator_execute_no_trigger(dag, requests_mock):
    requests_mock.post(
        "https://www.httpbin.org/api/v1/project/ABC-123/run",
        headers={"Content-Type": "application/json"},
        json={"projectId": "ABC-123", "runId": "1"},
    )

    mock_status = {
        "projectId": "ABC-123",
        "status": "COMPLETED",
        "runUrl": "https://example.com/run/1",
    }
    requests_mock.get(
        "https://www.httpbin.org/api/v1/project/abc-123/run/1",
        headers={"Content-Type": "application/json"},
        json=mock_status,
    )

    dagrun = dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=DATA_INTERVAL_START,
        data_interval=(DATA_INTERVAL_START, DATA_INTERVAL_END),
        start_date=DATA_INTERVAL_END,
        run_type=DagRunType.MANUAL,
    )
    ti = dagrun.get_task_instance(task_id=TEST_TASK_ID)
    ti.task = dag.get_task(task_id=TEST_TASK_ID)
    ti.run(ignore_ti_state=True)

    assert ti.state == TaskInstanceState.SUCCESS
    json = requests_mock.request_history[0].json()
    assert json["inputParams"]["input_date"][0:4] == str(DATA_INTERVAL_START.year)
    print(json)
    assert json["updateCache"] is False
