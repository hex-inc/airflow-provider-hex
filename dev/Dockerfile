ARG IMAGE_NAME="apache/airflow:2.3.3-python3.9"
FROM ${IMAGE_NAME}
USER root
COPY --chown=airflow:root airflow_provider_hex /home/airflow/airflow-provider-hex/airflow_provider_hex
COPY --chown=airflow:root setup.cfg /home/airflow/airflow-provider-hex/setup.cfg
COPY --chown=airflow:root setup.py /home/airflow/airflow-provider-hex/setup.py
COPY --chown=airflow:root VERSION.txt /home/airflow/airflow-provider-hex/VERSION.txt

USER airflow
WORKDIR /home/airflow
RUN pip install /home/airflow/airflow-provider-hex
