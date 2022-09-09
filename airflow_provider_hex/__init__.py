import importlib.metadata
import os
import sys

__version__ = importlib.metadata.version("airflow_provider_hex")


def verify():
    tag = os.getenv("CIRCLE_TAG")

    if tag != __version__:
        info = "Git tag: {0} does not match the version of this app: {1}".format(
            tag, __version__
        )
        sys.exit(info)


def get_provider_info():
    return {
        "package-name": "airflow-provider-hex",
        "name": "Airflow Provider Hex",
        "description": "Airflow hooks and operators for Hex",
        "versions": [__version__],
        "hook-class-names": [
            "airflow_provider_hex.hooks.hex.HexHook",
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow_provider_hex.hooks.hex.HexHook",
                "connection-type": "hex",
            }
        ],
    }
