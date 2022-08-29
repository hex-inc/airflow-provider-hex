.PHONY: dev clean init

dev:
	docker-compose -f dev/docker-compose.yaml up -d

clean:
	docker-compose -f dev/docker-compose.yaml down --volumes --remove-orphans

init:
	docker-compose up -f dev/docker-compose.yaml airflow-init