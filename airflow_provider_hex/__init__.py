import importlib.metadata

__version__ = importlib.metadata.version("airflow_provider_hex")


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
