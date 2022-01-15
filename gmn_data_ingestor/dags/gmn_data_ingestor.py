from datetime import timedelta

from airflow.operators.python import get_current_context, PythonOperator
from airflow.utils.dates import days_ago
from airflow.decorators import dag

# from kafka import KafkaProducer

from lib.extract import save_extracted_data_file
from lib.gmn_data_directory import GMNDataDirectory, GMN_DATA_START_DATE
from lib.gmn_traj_summary_reader import read_traj_summary_file_as_dataframe

EXTRACTED_DATA_DIRECTORY = '~/extracted_data'


def gmn_data_to_kafka(day_offset: int = 0):
    context = get_current_context()
    target_date = context['logical_date'] + timedelta(days=day_offset)
    print(f"Extracting data from {target_date} in dag run with logical date {context['logical_date']} "
          f"on current execution date {context['execution_date']}")

    # Find target_date filename by looking at the directory listing
    gmn_data_directory = GMNDataDirectory()
    file_content = gmn_data_directory.get_daily_file_content_by_date(target_date, context['execution_date'])

    # Write file to ~/extracted_date/{execution_date}/
    extracted_file_path = save_extracted_data_file(EXTRACTED_DATA_DIRECTORY, target_date, context['logical_date'],
                                                   context['execution_date'], file_content)

    trajectory_df = read_traj_summary_file_as_dataframe(extracted_file_path)
    print(f"Shape of the data = {trajectory_df.shape}\n")
    print("First 5 rows of the DataFrame: ")
    print(trajectory_df.head())


default_args = {
    "owner": "owner1",
    "retires": 5,
    "retry_delay": timedelta(minutes=15),
}


@dag("gmn_data_ingestor_daily_extract_dag", tags=['daily'],
     start_date=GMN_DATA_START_DATE, default_args=default_args, schedule_interval="0 1 * * *", catchup=False)
def gmn_data_ingestor_daily_extract_dag():
    for day_offset in range(-9, 1):
        PythonOperator(
            task_id=f'batch_extract_day.{day_offset}',
            python_callable=gmn_data_to_kafka,
            op_kwargs={'day_offset': day_offset})


@dag("gmn_data_ingestor_historical_extract_dag", tags=['historical'],
     start_date=GMN_DATA_START_DATE, default_args=default_args, schedule_interval="@once", catchup=True)
def gmn_data_ingestor_historical_extract_dag():
    PythonOperator(
        task_id='batch_extract_day_historical',
        python_callable=gmn_data_to_kafka,
        op_kwargs={})


globals()['gmn_data_ingestor_daily_extract_dag'] = gmn_data_ingestor_daily_extract_dag()
globals()['gmn_data_ingestor_historical_extract_dag'] = gmn_data_ingestor_historical_extract_dag()

# https://airflow.apache.org/docs/apache-airflow/stable/executor/debug.html
if __name__ == "__main__":
    dag = globals()['gmn_data_ingestor_daily_extract_dag']
    dag.clear()
    dag.run(start_date=days_ago(1), end_date=days_ago(0))  # runs yesterdays dag
