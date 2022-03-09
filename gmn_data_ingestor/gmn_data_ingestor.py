from datetime import timedelta, datetime

import os

from airflow.operators.python import get_current_context, PythonOperator
from airflow.utils.dates import days_ago
from airflow.decorators import dag

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from gmn_python_api.data_directory import DATA_START_DATE
from gmn_python_api.data_directory import get_daily_file_content_by_date, \
    get_file_content_from_url
from gmn_python_api.trajectory_summary_reader import \
    read_trajectory_summary_as_dataframe, DATETIME_FORMAT

EXTRACTED_DATA_DIRECTORY = '~/extracted_data'
AVRO_SCHEMA_PATH = f"{os.path.dirname(__file__)}/avro/trajectory_summary_schema.avsc"
AVRO_SCHEMA = avro.load(AVRO_SCHEMA_PATH)


def save_extracted_daily_trajectory_summary_file(extracted_data_directory: str,
                                                 target_date: datetime,
                                                 logical_date: datetime,
                                                 execution_date: datetime,
                                                 file_content: str) -> str:
    execution_date_extracted_data_directory = os.path.join(
        os.path.expanduser(extracted_data_directory),
        execution_date.strftime('%Y%m%d'))
    os.makedirs(execution_date_extracted_data_directory, exist_ok=True)
    filename = f"target_{target_date}_logical_{logical_date}" \
               f"_execution_{execution_date}.log"
    file_path = os.path.join(execution_date_extracted_data_directory, filename)
    file = open(file_path, "w")
    file.write(file_content)
    file.close()

    return file_path


def save_all_trajectory_summary_file(extracted_data_directory: str,
                                     execution_date: datetime,
                                     file_content: str) -> str:
    execution_date_extracted_data_directory = os.path.join(
        os.path.expanduser(extracted_data_directory),
        execution_date.strftime('%Y%m%d') + "_historical")
    os.makedirs(execution_date_extracted_data_directory, exist_ok=True)
    filename = f"execution_{execution_date.strftime('%Y%m%d')}_historical.log"
    file_path = os.path.join(execution_date_extracted_data_directory, filename)
    file = open(file_path, "w")
    file.write(file_content)
    file.close()

    return file_path


def delivery_trajectory_summary(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def gmn_data_to_kafka_daily(day_offset: int = 0):
    print(day_offset)
    context = get_current_context()
    target_date = context['logical_date'] + timedelta(days=day_offset)
    print(
        f"Extracting daily data from {target_date} in dag run with logical date "
        f"{context['logical_date']} "
        f"on current execution date {context['execution_date']}"
        f" day_offset {day_offset}")

    # Find target_date filename by looking at the directory listing
    file_content = get_daily_file_content_by_date(target_date,
                                                  context['execution_date'])

    # Write file to ~/extracted_date/{execution_date}/
    extracted_file_path = save_extracted_daily_trajectory_summary_file(
        EXTRACTED_DATA_DIRECTORY,
        target_date, context['logical_date'],
        context['execution_date'],
        file_content)

    trajectory_df = read_trajectory_summary_as_dataframe(extracted_file_path)
    print(f"Shape of the data = {trajectory_df.shape}\n")

    trajectory_df['IAU (code)'] = trajectory_df['IAU (code)'].astype('unicode')
    trajectory_df['Participating (stations)'] = trajectory_df[
        'Participating (stations)'].astype('unicode')
    trajectory_df['Beginning (UTC Time)'] = trajectory_df[
        'Beginning (UTC Time)'].dt.strftime(DATETIME_FORMAT)

    trajectory_df.columns = trajectory_df.columns.str.replace('[^0-9a-zA-Z]+', '_')
    trajectory_df.columns = trajectory_df.columns.str.rstrip('_')
    trajectory_df.columns = trajectory_df.columns.str.lstrip('_')
    trajectory_df.columns = trajectory_df.columns.str.replace('Q_AU', 'q_au_')
    trajectory_df.columns = trajectory_df.columns.str.lower()

    avroProducer = AvroProducer({
        'bootstrap.servers': 'kafka-broker:29092',
        'on_delivery': delivery_trajectory_summary,
        'schema.registry.url': 'http://schema-registry:8081'
    }, default_key_schema=None, default_value_schema=AVRO_SCHEMA)

    for index, row in trajectory_df.iterrows():
        print(f"Sending index {index}, row = {row} to kafka")
        avroProducer.produce(topic='extracted', value=row.to_dict(), key=None)
        avroProducer.poll(0)
        print(f"Successfully sent index {index}")
    avroProducer.flush()


def gmn_data_to_kafka_historical():
    context = get_current_context()
    print(
        f"Historically extracting data from traj_summary_all.txt "
        f"execution date {context['execution_date']}")

    # Find target_date filename by looking at the directory listing
    file_content = get_file_content_from_url("https://globalmeteornetwork.org/data/traj_summary_data/traj_summary_all.txt")

    # Write file to ~/extracted_date/{execution_date}/
    extracted_file_path = save_all_trajectory_summary_file(
        EXTRACTED_DATA_DIRECTORY,
        context['execution_date'],
        file_content)

    trajectory_df = read_trajectory_summary_as_dataframe(extracted_file_path)
    print(f"Shape of the data = {trajectory_df.shape}\n")

    trajectory_df['IAU (code)'] = trajectory_df['IAU (code)'].astype('unicode')
    trajectory_df['Participating (stations)'] = trajectory_df[
        'Participating (stations)'].astype('unicode')
    trajectory_df['Beginning (UTC Time)'] = trajectory_df[
        'Beginning (UTC Time)'].dt.strftime(DATETIME_FORMAT)

    trajectory_df.columns = trajectory_df.columns.str.replace('[^0-9a-zA-Z]+', '_')
    trajectory_df.columns = trajectory_df.columns.str.rstrip('_')
    trajectory_df.columns = trajectory_df.columns.str.lstrip('_')
    trajectory_df.columns = trajectory_df.columns.str.replace('Q_AU', 'q_au_')
    trajectory_df.columns = trajectory_df.columns.str.lower()

    avroProducer = AvroProducer({
        'bootstrap.servers': 'kafka-broker:29092',
        'on_delivery': delivery_trajectory_summary,
        'schema.registry.url': 'http://schema-registry:8081'
    }, default_key_schema=None, default_value_schema=AVRO_SCHEMA)

    for index, row in trajectory_df.iterrows():
        print(f"Sending index {index}, row = {row.to_dict()} to kafka")
        avroProducer.produce(topic='extracted', value=row.to_dict(), key=None)
        avroProducer.poll(0)
        print(f"Successfully sent index {index}")
    avroProducer.flush()


default_args = {
    "owner": "gmndatauser",
    "retires": 5,
    "retry_delay": timedelta(minutes=15),
}


@dag("gmn_data_ingestor_daily_extract_dag", tags=['daily'],
     start_date=DATA_START_DATE, default_args=default_args,
     schedule_interval="0 1 * * *", catchup=False)
def gmn_data_ingestor_daily_extract_dag():
    for day_offset in range(-9, 1):
        PythonOperator(
            task_id=f'batch_extract_day.{day_offset}',
            python_callable=gmn_data_to_kafka_daily,
            op_kwargs={'day_offset': day_offset})


@dag("gmn_data_ingestor_historical_extract_dag", tags=['historical'],
     start_date=DATA_START_DATE, default_args=default_args,
     schedule_interval="@once", catchup=False)
def gmn_data_ingestor_historical_extract_dag():
    PythonOperator(
        task_id='batch_extract_day_historical',
        python_callable=gmn_data_to_kafka_historical,
        op_kwargs={})


globals()[
    'gmn_data_ingestor_daily_extract_dag'
] = gmn_data_ingestor_daily_extract_dag()

globals()[
    'gmn_data_ingestor_historical_extract_dag'
] = gmn_data_ingestor_historical_extract_dag()

# https://airflow.apache.org/docs/apache-airflow/stable/executor/debug.html
if __name__ == "__main__":
    dag = globals()['gmn_data_ingestor_daily_extract_dag']
    dag.clear()
    dag.run(start_date=days_ago(1), end_date=days_ago(0))  # runs yesterdays dag
