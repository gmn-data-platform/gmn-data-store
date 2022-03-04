.ONESHELL:
SHELL=/bin/bash

init_services: init_database_services init_ingestor_services
run_services: run_all_services
run_tests: run_database_tests run_ingestor_tests
stop_services: stop_all_services
stop_and_clean_services: stop_and_clean_all_services

init_database_services:
	echo "Initializing database services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor up --abort-on-container-exit db-init

run_database_services:
	echo "Running database services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor up -d db

run_database_tests:
	echo "Running database tests"

stop_database_services:
	echo "Stopping database services"


init_ingestor_services:
	echo "Initializing ingestor services"
	cd gmn_data_ingestor
	echo -e "AIRFLOW_UID=$(shell id -u)" > .env
	cd ../
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor up --abort-on-container-exit kafka-init
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor up --abort-on-container-exit airflow-init
	# docker-compose -p gmn_data_ingestor up ksqldb-init

test_run_main_dag:
	echo "Test running the main dag"
	docker exec -it gmn_data_ingestor-airflow-worker-1 /bin/bash -c "export AIRFLOW__CORE__EXECUTOR=DebugExecutor && python /opt/airflow/dags/gmn_data_ingestor.py"

run_ingestor_tests:
	echo "Running ingestor tests"
	docker exec -it gmn_data_ingestor-airflow-worker-1 pytest /opt/airflow/tests

run_all_services:
	echo "Running all services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor up -d

view_all_logs:
	echo "Viewing all logs"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor logs -f

stop_all_services:
	echo "Stopping ingestor services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor down --remove-orphans

stop_and_clean_all_services:
	echo "Stopping and cleaning all services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor down -v --rmi all

restart_all_services:
	echo "Restarting all services"
	docker-compose --env-file ./gmn_data_ingestor/.env -p gmn_data_ingestor restart

generate_avro_schema:
	# TODO move avro init to gmn-python-api
	cd gmn_data_ingestor/avro
	python -m pip install pandavro==1.6.0 avro==1.11.0 gmn-python-api==0.0.1
	python generate_trajectory_summary_avro_schema.py