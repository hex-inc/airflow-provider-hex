import logging

import pytest
from airflow import AirflowException

from airflow_provider_hex.hooks.hex import HexHook

log = logging.getLogger(__name__)


mock_run = {
    "projectId": "abc-123",
    "runId": "1",
    "runStatusUrl": "https://www.httpbin.org/api/v1/project/abc-123/run/1",
    "runUrl": "https://www.httpbin.org/api/v1/project/my-run-url",
}


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
        assert requests_mock.last_request.json() == {
            "inputParams": {"param": "var"},
            "updateCache": False,
        }

    def test_run_project_empty_inputs(self, requests_mock):
        requests_mock.post(
            "https://www.httpbin.org/api/v1/project/abc-123/run",
            headers={"Content-Type": "application/json"},
            json={"data": "mocked response"},
        )

        hook = HexHook(hex_conn_id="hex_conn")
        response = hook.run_project("abc-123")
        assert response == {"data": "mocked response"}
        assert requests_mock.last_request.json() == {
            "updateCache": False,
        }

    def test_run_status(self, requests_mock):
        requests_mock.get(
            "https://www.httpbin.org/api/v1/project/abc-123/run/1",
            headers={"Content-Type": "application/json"},
            json={"data": "mocked response"},
        )

        hook = HexHook(hex_conn_id="hex_conn")
        response = hook.run_status("abc-123", "1")
        assert response == {"data": "mocked response"}

    def test_run_poll_success(self, requests_mock):
        requests_mock.post(
            "https://www.httpbin.org/api/v1/project/abc-123/run",
            headers={"Content-Type": "application/json"},
            json=mock_run,
        )

        mock_status = {"projectId": "abc-123", "status": "COMPLETED"}

        requests_mock.get(
            "https://www.httpbin.org/api/v1/project/abc-123/run/1",
            headers={"Content-Type": "application/json"},
            json=mock_status,
        )

        hook = HexHook(hex_conn_id="hex_conn")

        response = hook.run_and_poll("abc-123", inputs=None)
        assert response["status"] == "COMPLETED"

    def test_run_poll_pending_and_success(self, requests_mock):
        requests_mock.post(
            "https://www.httpbin.org/api/v1/project/abc-123/run",
            headers={"Content-Type": "application/json"},
            json=mock_run,
        )

        mock_status = {"projectId": "abc-123", "status": "PENDING"}

        mock_status_2 = {"projectId": "abc-123", "status": "COMPLETED"}

        header = {"Content-Type": "application/json"}
        requests_mock.register_uri(
            "GET",
            "https://www.httpbin.org/api/v1/project/abc-123/run/1",
            [
                {"headers": header, "json": mock_status},
                {"headers": header, "json": mock_status_2},
            ],
        )

        hook = HexHook(hex_conn_id="hex_conn")

        response = hook.run_and_poll("abc-123", inputs=None, poll_interval=1)
        assert response["status"] == "COMPLETED"

    def test_run_poll_pending_and_error(self, requests_mock):
        requests_mock.post(
            "https://www.httpbin.org/api/v1/project/abc-123/run",
            headers={"Content-Type": "application/json"},
            json=mock_run,
        )

        mock_status = {"projectId": "abc-123", "status": "PENDING"}

        mock_status_2 = {"projectId": "abc-123", "status": "UNABLE_TO_ALLOCATE_KERNEL"}

        header = {"Content-Type": "application/json"}
        requests_mock.register_uri(
            "GET",
            "https://www.httpbin.org/api/v1/project/abc-123/run/1",
            [
                {"headers": header, "json": mock_status},
                {"headers": header, "json": mock_status_2},
            ],
        )

        hook = HexHook(hex_conn_id="hex_conn")

        with pytest.raises(AirflowException, match=r"Project Run failed with status.*"):
            hook.run_and_poll("abc-123", inputs=None, poll_interval=1)
