from airflow import DAG
from datetime import datetime, timedelta

with DAG(
    dag_id='hello_world',
    description='Hello World DAG',
    start_date=datetime(2023, 4, 4, 17),
    schedule_interval='@daily',
) as dag:
    pass

