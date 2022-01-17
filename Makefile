.ONESHELL:
SHELL=/bin/bash

init_services: init_database_services init_ingestor_services
run_services: run_database_services run_ingestor_services
run_tests: run_database_tests run_ingestor_tests
stop_services: stop_database_services stop_ingestor_services


init_database_services:
	echo "Initializing database services"

run_database_services:
	echo "Running database services"

run_database_tests:
	echo "Running database tests"

stop_database_services:
	echo "Stopping database services"


init_ingestor_services:
	echo "Initializing ingestor services"
	cd gmn_data_ingestor
	echo -e "AIRFLOW_UID=$(shell id -u)" > .env
	echo -e "_PIP_ADDITIONAL_REQUIREMENTS=$$(cat requirements_additional.txt | tr "\n" " ")" >> .env
	docker compose -p gmn_data_ingestor up airflow-init kafka-init

run_ingestor_services:
	echo "Running ingestor services"
	cd gmn_data_ingestor
	docker compose up -d

test_run_main_dag:
	echo "Test running the main dag"
	docker exec -it gmn_data_ingestor-airflow-worker-1 /bin/bash -c "export AIRFLOW__CORE__EXECUTOR=DebugExecutor && python /opt/airflow/dags/gmn_data_ingestor.py"

run_ingestor_tests:
	echo "Running ingestor tests"
	docker exec -it gmn_data_ingestor-airflow-worker-1 pytest /opt/airflow/tests

stop_ingestor_services:
	echo "Stopping ingestor services"
	cd gmn_data_ingestor
	docker compose down

stop_and_clean_all_services:
	echo "Stopping and cleaning all services"
	cd gmn_data_ingestor
	docker compose down -v --rmi all
