from typing import Any, Dict

from airflow.providers.http.hooks import BaseHook


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
            "hidden_fields": ["port", "host", "login", "schema", "extra"],
            "relabeling": {"password": "Hex API Token"},
        }

    def __init__(self, hex_conn_id: str = default_conn_name):
        super().__init__()
        pass
