from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Set the path to your scraper.py file
scraper_script_path = '/opt/airflow/scripts/scraper.py'

# Set the path to your virtual environment
virtualenv_path = '/opt/airflow/venv'

# DAG configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Instantiate the DAG
dag = DAG(
    'scraper_dag',
    default_args=default_args,
    description='A DAG to scrape a website and upload the file to Azure Blob Storage daily',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 8, 22),
    catchup=False
)

# Define the task
run_scraper_task = BashOperator(
    task_id='run_scraper',
    bash_command=f'source {virtualenv_path}/bin/activate && python {scraper_script_path}',
    dag=dag
)
