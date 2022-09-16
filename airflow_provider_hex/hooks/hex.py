import datetime
import time
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, Optional, cast
from urllib.parse import urljoin

import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

from airflow_provider_hex.types import RunResponse, StatusResponse

PENDING = "PENDING"
RUNNING = "RUNNING"
KILLED = "KILLED"
ERRORED = "ERRORED"
COMPLETE = "COMPLETED"
UNABLE_TO_ALLOCATE_KERNEL = "UNABLE_TO_ALLOCATE_KERNEL"
VALID_STATUSES = [
    PENDING,
    RUNNING,
    ERRORED,
    COMPLETE,
    UNABLE_TO_ALLOCATE_KERNEL,
    KILLED,
]
TERMINAL_STATUSES = [COMPLETE, ERRORED, UNABLE_TO_ALLOCATE_KERNEL, KILLED]


class HexHook(BaseHook):
    """Hex Hook into the API

    :param hex_conn_id: `Conn ID` of the Connection used to configure this hook.
    :type hex_conn_id: str
    """

    conn_name_attr = "hex_conn_id"
    default_conn_name = "hex_default"
    conn_type = "hex"
    hook_name = "Hex Connection"

    @classmethod
    def get_ui_field_behaviour(cls) -> Dict[str, Any]:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["port", "login", "schema", "extra"],
            "relabeling": {"password": "Hex API Token"},
            "placeholders": {
                "password": "API Token from your Hex settings screen",
                "host": "Hex API base url, https://app.hex.tech for most customers.",
            },
        }

    def __init__(self, hex_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.hex_conn_id: str = hex_conn_id
        self.base_url: str = ""

    def get_conn(self) -> requests.Session:
        """
        Returns http session for use with requests
        """
        session = requests.Session()
        conn = self.get_connection(self.hex_conn_id)
        try:
            __version__ = version("airflow_provider_hex")
        except PackageNotFoundError:
            __version__ = "UnknownVersion"

        user_agent = "HexAirflowHook/" + __version__
        session.headers.update({"User-Agent": user_agent})

        if conn.host and "://" in conn.host:
            self.base_url = conn.host
        else:
            schema = "https"
            host = conn.host if conn.host else ""
            self.base_url = schema + "://" + host

        if conn.password:
            auth_header = {"Authorization": f"Bearer {conn.password}"}
            session.headers.update(auth_header)
        else:
            raise AirflowException("Hex Secret token is required for this hook")

        return session

    def run(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Performs the request and returns the results from the API

        :param method: the HTTP method, e.g. POST, GET
        :type method: str
        :param endpoint: the endpoint to be called e.g. /run
        :type endpoint: str
        :param data: payload to be sent in the request body
        :type data: dict
        """
        session = self.get_conn()
        url = urljoin(self.base_url, endpoint)
        if method == "GET":
            req = requests.Request(method, url, params=data)
        if method == "POST":
            req = requests.Request(method, url, json=data)
        else:
            req = requests.Request(method, url, data=data)

        prepped_request = session.prepare_request(req)
        self.log.info("Sending '%s' to url: %s", method, url)
        response = session.send(prepped_request)
        response.raise_for_status()

        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                self.log.error("Failed to decode response from API.")
                self.log.error("API returned: %s", response.text)
                raise AirflowException(
                    "Unexpected response from Hex API. Failed to decode to JSON."
                )
            return response_json

        return {"response": response.text}

    def run_project(
        self,
        project_id: str,
        inputs: Optional[Dict[str, Any]] = None,
        update_cache: bool = False,
    ) -> RunResponse:
        endpoint = f"/api/v1/project/{project_id}/run"
        method = "POST"

        response = cast(
            RunResponse,
            self.run(
                method=method,
                endpoint=endpoint,
                data={"inputParams": inputs, "updateCache": update_cache},
            ),
        )
        return response

    def run_status(self, project_id, run_id) -> StatusResponse:
        endpoint = f"api/v1/project/{project_id}/run/{run_id}"
        method = "GET"

        response = cast(
            StatusResponse, self.run(method=method, endpoint=endpoint, data=None)
        )
        return response

    def cancel_run(self, project_id, run_id) -> str:
        endpoint = f"api/v1/project/{project_id}/run/{run_id}"
        method = "DELETE"

        self.run(method=method, endpoint=endpoint)
        return run_id

    def run_and_poll(
        self,
        project_id: str,
        inputs: Optional[dict],
        update_cache: bool = False,
        poll_interval: int = 3,
        poll_timeout: int = 600,
        kill_on_timeout: bool = True,
    ):
        run_response = self.run_project(project_id, inputs, update_cache)
        run_id = run_response["runId"]

        poll_start = datetime.datetime.now()
        while True:
            run_status = self.run_status(project_id, run_id)
            project_status = run_status["status"]

            self.log.info(
                f"Polling Hex Project {project_id}. Status: {project_status}."
            )
            if project_status not in VALID_STATUSES:
                raise AirflowException(f"Unhandled status: {project_status}")

            if project_status == COMPLETE:
                break

            if project_status in TERMINAL_STATUSES:
                raise AirflowException(
                    f"Project Run failed with status {project_status}. "
                    f"See Run URL for more info {run_response['runUrl']}"
                )

            if (
                kill_on_timeout
                and datetime.datetime.now()
                > poll_start + datetime.timedelta(seconds=poll_timeout)
            ):

                self.log.error(
                    "Failed to complete project within %s seconds, cancelling run",
                    poll_timeout,
                )
                try:
                    self.cancel_run(project_id, run_id)
                finally:
                    raise AirflowException(
                        f"Project {project_id} with run: {run_id}' timed out after "
                        f"{datetime.datetime.now() - poll_start}. "
                        f"Last status was {project_status}."
                    )

            time.sleep(poll_interval)
        return run_status
