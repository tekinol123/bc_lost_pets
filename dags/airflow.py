from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

def greet():
    print('Hello World')

with DAG(
    dag_id='hello_world',
    default_args=default_args,
    description='Hello World DAG',
    start_date=datetime(2023, 4, 6),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
    )
    task1

