from airflow import DAG
from functions.utils import *
import datetime 
from datetime import timedelta
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

tables = ["flights", "boarding_passes",
          "bookings","tickets","airports_data",
          "aircrafts_data",
          "ticket_flights"] 
defaul_args = {
    'owner': 'airflow', 
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG (
    'postgres_to_mongo',
    default_args = defaul_args,
    description = 'Postgres to Mongo',
    schedule_interval = "@daily",
    catchup = False
) as dag :
    start_task = EmptyOperator(task_id = 'start_task')
    
    with TaskGroup("fetch_postgres_data") as fetch_postgres_data:
        extract_tasks = []
        for table in tables:
            extract_task = PythonOperator(
                task_id = f"fetch_table_from_postgres_{table}",
                python_callable = fetch_table_from_postresql,
                op_kwargs = {
                    'table_name': table
                }
            )
            extract_tasks.append(extract_task)
    
    end_task = EmptyOperator(task_id = 'end_task')
    start_task >> fetch_postgres_data >> end_task


