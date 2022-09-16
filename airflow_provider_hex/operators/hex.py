from typing import Any, Dict, Optional

from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults

from airflow_provider_hex.hooks.hex import HexHook


class HexRunProjectOperator(BaseOperator):
    """Runs a Hex Project, and optionally waits until completion.

    :param project_id: Hex Project ID
    :type project_id: str
    :param hex_conn_id: connection run the operator with
    :type hex_conn_id: str
    :param synchronous: if true, wait for the project run to complete otherwise request
        a run but do not wait for completion. Useful for long-running projects that
        block the DAG from completing.
    :type synchronous: bool
    :param wait_seconds: interval to wait, in seconds, between successive API polls.
    :type wait_seconds: int
    :param timeout: maximum time to wait for a sync to complete before aborting the run.
        if kill_on_timeout is true, also attempt to end the project run
    :type timeout: int
    :param kill_on_timeout: if true attempt to stop the project if the timeout is
        reached. If false, the project will continue running indefinitely in the
        background until completion.
    :type kill_on_timeout: bool
    :param input_paramters: additional input parameters, a json-serializable dictionary
        of variable_name: value pairs.
    :type input_parameters: dict
    :param update_cache: When true, this run will update the cached state of the
        published app with the latest run results.
        Additionally, any SQL cells that have caching enabled will be re-executed as
        part of this run. Note that this cannot be set to true if custom input
        parameters are provided.
    """

    template_fields = ["project_id"]
    ui_color = "#F5C0C0"

    @apply_defaults
    def __init__(
        self,
        project_id: str,
        hex_conn_id: str = "hex_default",
        synchronous: bool = True,
        wait_seconds: int = 3,
        timeout: int = 3600,
        kill_on_timeout: bool = True,
        input_parameters: Optional[Dict[str, Any]] = None,
        update_cache: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.project_id = project_id
        self.hex_conn_id = hex_conn_id
        self.synchronous = synchronous
        self.wait_seconds = wait_seconds
        self.timeout = timeout
        self.kill_on_timeout = kill_on_timeout
        self.input_parameters = input_parameters
        self.update_cache = update_cache

    def execute(self, context: Context) -> Any:
        hook = HexHook(self.hex_conn_id)

        if self.synchronous:
            self.log.info("Starting Hex Project")
            resp = hook.run_and_poll(
                self.project_id,
                inputs=self.input_parameters,
                update_cache=self.update_cache,
                poll_interval=self.wait_seconds,
                poll_timeout=self.timeout,
                kill_on_timeout=self.kill_on_timeout,
            )
            self.log.info("Hex Project completed successfully")

        else:
            self.log.info("Starting Hex Project asynchronously")
            resp = hook.run_project(self.project_id, inputs=self.input_parameters)
            self.log.info("Hex Project started successfully.")

        self.log.info(resp)
        return resp
