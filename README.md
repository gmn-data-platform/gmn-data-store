# GMN Data Store
Code for the database schema and GMN data ingestor.

## Requirements
| Prerequisite                                                      | Description                                             |
|-------------------------------------------------------------------|---------------------------------------------------------|
| [Docker](https://www.docker.com/)                                 | Container management tool                               |
| [Docker Compose v2](https://docs.docker.com/compose/cli-command/) | A tool for defining multi-container apps                |
| [GNU Make 4.1+](https://www.gnu.org/software/make/)               | A tool which allows an easy way to run project commands |

Refer to the [gmn-data-platform](https://github.com/gmn-data-platform/gmn-data-platform) repository for optional PyCharm setup.

## Database Schema
...

## GMN Data Ingestor

### Running using Docker Compose
```sh
make init_ingestor_services
make run_ingestor_services
```
Go to http://localhost:8080 for the Airflow UI.

Check logs with:
```sh
docker compose logs
```

Access the Airflow CLI like so:
```sh
./airflow-cli version
./airflow-cli bash
./airflow-cli python
```

Use the Airflow rest API like so:
```sh
curl -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags"
```

Stop database services with:
```sh
make stop_ingestor_services
```

See the [makefile](Makefile) for more commands.

---



## Relevant links
https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html

https://medium.com/ninjavan-tech/setting-up-a-complete-local-development-environment-for-airflow-docker-pycharm-and-tests-3577ddb4ca94

https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker

https://www.youtube.com/watch?v=tdvh7unRe18

https://stackoverflow.com/questions/49818282/failing-to-get-pycharm-to-work-with-remote-interpreter-on-docker/65345574#65345574