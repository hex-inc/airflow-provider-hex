# Hex Airflow Provider

Provides an Airflow Operator and Hook to trigger Hex project runs.

This [Airflow Provider Package](https://airflow.apache.org/docs/apache-airflow-providers/)
provides Hooks and Operators for interacting with the Hex API.

## Requirements

* Airflow >=2.2
* Hex API Token

## Initial Setup

Install the package.

```
pip install airflow-provider-hex
```

After creating a Hex API token, set up your Airflow Connection Credentials in the Airflow
UI.

![Connection Setup](https://raw.githubusercontent.com/hex-inc/airflow-provider-hex/main/docs/hex-connection-setup.png)

* Connection ID: `hex_default`
* Connection Type: `Hex Connection`
* Host: `https://app.hex.tech`
* Hex API Token: `your-token-here`

## Operators

The [`airflow_provider_hex.operators.hex.HexRunProjectOperator`](/airflow_provider_hex/operators/hex.py)
Operator runs Hex Projects, either synchronously or asynchronously.

In the synchronous mode, the Operator will start a Hex Project run and then
poll the run until either an error or success status is returned, or until
the poll timeout. If the timeout occurs, the default behaviour is to attempt to
cancel the run.

In the asynchronous mode, the Operator will request that a Hex Project is run,
but will not poll for completion. This can be useful for long-running projects.

The operator accepts inputs in the form of a dictionary. These can be used to
override existing input elements in your Hex project.

## Hooks

The [`airflow_provider_hex.hooks.hex.HexHook`](/airflow_provider_hex/hooks/hex.py)
provides a low-level interface to the Hex API.

These can be useful for testing and development, as they provide both a generic
`run` method which sends an authenticated request to the Hex API, as well as
implementations of the `run` method that provide access to specific endpoints.


## Examples

A simplified example DAG demonstrates how to use the [Airflow Operator](/example_dags/example_hex.py)

```python
from airflow_provider_hex.operators.hex import HexRunProjectOperator

PROJ_ID = 'abcdef-ghijkl-mnopq'
...
sync_run = HexRunProjectOperator(
    task_id="run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
    input_parameters={'myParam': 42}
)
```
