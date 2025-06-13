# Airflow Provider for Hex

[![PyPI version](https://badge.fury.io/py/airflow-provider-hex.svg)](https://badge.fury.io/py/airflow-provider-hex)

This [Airflow Provider Package](https://airflow.apache.org/docs/apache-airflow-providers/) provides Hooks and Operators for interacting with the Hex API, allowing you to trigger and manage Hex project runs in your Apache Airflow DAGs.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Initial Setup](#initial-setup)
- [Operators](#operators)
- [Hooks](#hooks)
- [Examples](#examples)
- [Development](#development)
- [Changelog](#changelog)

## Requirements

* Apache Airflow >= 2.2.0
* Python >= 3.7
* Hex API Token

## Installation

Install the package using pip:

```bash
pip install airflow-provider-hex
```

## Initial Setup

After creating a Hex API token, set up your Airflow Connection Credentials in the Airflow UI:

![Connection Setup](https://raw.githubusercontent.com/hex-inc/airflow-provider-hex/main/docs/hex-connection-setup.png)

* Connection ID: `hex_default`
* Connection Type: `Hex Connection`
* Host: `https://app.hex.tech`
* Hex API Token: `your-token-here`

## Operators

The [`HexRunProjectOperator`](/airflow_provider_hex/operators/hex.py) runs Hex Projects either synchronously or asynchronously.

- In synchronous mode, the Operator starts a Hex Project run and polls until completion or timeout.
- In asynchronous mode, the Operator requests a Hex Project run without waiting for completion.

The operator accepts inputs as a dictionary to override existing input elements in your Hex project. You can also include optional notifications for a run.

For more details, see the [Hex API documentation](https://learn.hex.tech/docs/develop-logic/hex-api/api-reference#operation/RunProject).

## Hooks

The [`HexHook`](/airflow_provider_hex/hooks/hex.py) provides a low-level interface to the Hex API. It's useful for testing and development, offering both a generic `run` method for authenticated requests and specific endpoint implementations.

## Examples

Here's a simplified example DAG demonstrating how to use the HexRunProjectOperator:

```python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow_provider_hex.operators.hex import HexRunProjectOperator
from airflow_provider_hex.types import NotificationDetails

PROJ_ID = 'abcdef-ghijkl-mnopq'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG('hex_example', default_args=default_args, schedule_interval=None)

notifications: list[NotificationDetails] = [
    {
        "type": "SUCCESS",
        "includeSuccessScreenshot": True,
        "slackChannelIds": ["HEX666SQG"],
        "userIds": [],
        "groupIds": [],
    }
]

sync_run = HexRunProjectOperator(
    task_id="run",
    hex_conn_id="hex_default",
    project_id=PROJ_ID,
    dag=dag,
    notifications=notifications
)
```

For more examples, check the [example_dags](/example_dags) directory.

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies: `pip install -e .[dev]`
3. Install pre-commit hooks: `pre-commit install`

To run tests:

```bash
make tests
```

To run linters:

```bash
make lint
```

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file for details on all changes and past releases.
