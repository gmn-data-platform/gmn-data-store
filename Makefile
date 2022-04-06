.ONESHELL:
SHELL=/bin/bash

init_all_services: init_database_services
run_all_tests: run_database_tests

init_database_services:
	echo "Initializing database services"
	docker-compose --profile=init up --abort-on-container-exit

run_database_tests:
	echo "Running database tests"

stop_database_services:
	echo "Stopping database services"
	docker-compose down --remove-orphans

view_all_logs:
	echo "Viewing all logs"
	docker-compos logs -f

stop_and_clean_all_services:
	echo "Stopping and cleaning all services"
	docker-compose down -v --rmi all

restart_all_services:
	echo "Restarting all services"
	docker-compose restart
