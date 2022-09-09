import logging

import pytest

from airflow_provider_hex.hooks.hex import HexHook

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def sample_conn(mocker):
    mocker.patch.dict(
        "os.environ",
        AIRFLOW_CONN_HEX_CONN="http://some:password@https%3A%2F%2Fwww.httpbin.org%2F",
    )


class TestHexHook:
    def test_run(self, requests_mock):
        requests_mock.get(
            "https://www.httpbin.org/endpoint",
            headers={"Content-Type": "application/json"},
            json={"data": "mocked response"},
        )

        hook = HexHook(hex_conn_id="hex_conn")
        response = hook.run(method="GET", endpoint="endpoint")
        assert response["data"] == "mocked response"

    def test_run_project(self, requests_mock):
        requests_mock.post(
            "https://www.httpbin.org/api/v1/project/abc-123/run",
            headers={"Content-Type": "application/json"},
            json={"data": "mocked response"},
        )

        hook = HexHook(hex_conn_id="hex_conn")
        response = hook.run_project("abc-123", inputs={"param": "var"})
        assert response == {"data": "mocked response"}
        assert requests_mock.last_request.json() == {"inputParams": {"param": "var"}}

    def test_run_status(self, requests_mock):
        requests_mock.get(
            "https://www.httpbin.org/api/v1/project/abc-123/run/1",
            headers={"Content-Type": "application/json"},
            json={"data": "mocked response"},
        )

        hook = HexHook(hex_conn_id="hex_conn")
        response = hook.run_status("abc-123", "1")
        assert response == {"data": "mocked response"}
