# GMN Data Store
Global Meteor Network database schema and data ingestion.

## Requirements
| Prerequisite                                                      | Description                                             |
|-------------------------------------------------------------------|---------------------------------------------------------|
| [Docker](https://www.docker.com/)                                 | Container management tool                               |
| [Docker Compose v2](https://docs.docker.com/compose/cli-command/) | A tool for defining multi-container apps                |
| [GNU Make 4.1+](https://www.gnu.org/software/make/)               | A tool which allows an easy way to run project commands |

## Setup environment variables with .env
Setup environment files:
```sh
# Linux/Mac
cp database/.env.default database/.env

# Or Windows
copy database/.env.default database/.env
```

Then input environment variables in `.env`  to match your own system/configuration.

## Running using Docker Compose
```sh
make init_services
make run_services
```

Main endpoints 
- Airflow UI - http://0.0.0.0:8080/
- Elastic - http://localhost:5601/
- Kibana - http://localhost:5601/

Check logs with:
```sh
make view_logs
```

### Airflow

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
make stop_services
```

See the [makefile](Makefile) for more commands.

---

## PyCharm setup steps (optional)
- Use the `.run` directory for run configurations for this project. These settings should be loaded automatically.
- Set docker-compose path in PyCharm to be `~/.local/bin/docker-compose-v2` where the file is executable and contains:
```sh
#!/bin/bash
docker compose "$@"
```
- Enable "Use Docker Compose v2 beta".
- Setup Python interpreter using Docker Compose.
- For debugging use the pycharm remote debugger (todo).
- Recommended non-bundled plugins: [Big Data Tools](https://plugins.jetbrains.com/plugin/12494-big-data-tools), [Makefile Language](https://plugins.jetbrains.com/plugin/9333-makefile-language), [.env files support](https://plugins.jetbrains.com/plugin/9525--env-files-support), [CSV](https://github.com/SeeSharpSoft/intellij-csv-validator)

## Relevant links
https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html

https://medium.com/ninjavan-tech/setting-up-a-complete-local-development-environment-for-airflow-docker-pycharm-and-tests-3577ddb4ca94

https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker

https://www.youtube.com/watch?v=tdvh7unRe18

https://stackoverflow.com/questions/49818282/failing-to-get-pycharm-to-work-with-remote-interpreter-on-docker/65345574#65345574
