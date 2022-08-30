ARG IMAGE_NAME="apache/airflow:2.3.3-python3.9"
FROM ${IMAGE_NAME}

USER root
COPY --chown=airflow:root airflow_provider_hex ${AIRFLOW_HOME}/airflow_provider_hex
COPY --chown=airflow:root  VERSION.txt ${AIRFLOW_HOME}/airflow_provider_hex/VERSION.txt
COPY --chown=airflow:root  setup.cfg ${AIRFLOW_HOME}/airflow_provider_hex/setup.cfg
COPY --chown=airflow:root  setup.py ${AIRFLOW_HOME}/airflow_provider_hex/setup.py

USER airflow
RUN pip install ${AIRFLOW_HOME}/airflow_provider_hex[dev]
