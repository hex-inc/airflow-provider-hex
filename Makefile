.PHONY: dev clean init tests lint

lint:
	mypy airflow_provider_hex
	isort airflow_provider_hex
	black airflow_provider_hex
	flake8 airflow_provider_hex

tests:
	pytest -s -vv

dev:
	docker-compose -f dev/docker-compose.yaml up -d

build:
	docker-compose -f dev/docker-compose.yaml up --build

clean:
	docker-compose -f dev/docker-compose.yaml down --volumes --remove-orphans

init:
	docker-compose up -f dev/docker-compose.yaml airflow-init
