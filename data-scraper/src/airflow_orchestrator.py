from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
import subprocess
from airflow.utils.dates import days_ago
import time

# Define functions to run subprocesses
def run_licensee_scraper():
    subprocess.run(["python3", "./src/licensee_scraper.py"])

def run_violation_scraper():
    subprocess.run(["python3", "./src/violation_scraper.py"])


def merge_files():
    time.sleep(1)

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'etl_workflow_with_dynamic_directory',
    default_args=default_args,
    description='An ETL workflow with dynamic directory creation',
    schedule_interval=timedelta(days=1),
)

create_directory = BashOperator(
    task_id='create_directory',
    bash_command='mkdir -p /app/data/{{ ds }}'
)

# Define the tasks
download_licensee = BashOperator(
    task_id='download_license',
    bash_command="python3 /app/src/licensee_scraper.py /app/data/{{ ds }}/licenses.csv",
    dag=dag,
)

# Define the tasks
download_violations = BashOperator(
    task_id='download_violations',
    bash_command="python3 /app/src/violation_scraper.py /app/data/{{ ds }}/violations.csv",
    dag=dag
)

# Define the tasks
run_merge_files = PythonOperator(
    task_id='merge_files',
    python_callable=merge_files,
    dag=dag,
)


create_directory >> [ download_licensee, download_violations ] >> run_merge_files
