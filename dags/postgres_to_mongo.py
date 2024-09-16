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

stats = [
    "flights_over_time",
    "total_flights_per_week",
    "delayed_flights_per_week",
    "average_delay_time_per_week",
    "top_airports_by_departures",
    "average_passengers_per_flight_per_week",
    "last_weeks_revenue",
    "flights_lines"
    
]
kpis = [v for v in stats if "week" in v]
aggs = [v for v in stats if "week" not in v ]






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
    
    with TaskGroup("compute_kpis") as compute_kpis_group:
        compute_kpis_tasks = []
        for kpi in kpis:
            compute_task = PythonOperator(
                task_id = f"compute_{kpi}",
                python_callable = compute,
                op_kwargs = {
                    'stats': kpi
                }
            )
            compute_kpis_tasks.append(compute_task)
    with TaskGroup("compute_aggs") as compute_aggs_group:
        compute_aggs_tasks = []
        for agg in aggs:
            compute_task = PythonOperator(
                task_id = f"compute_{agg}", 
                python_callable = compute,
                op_kwargs = {
                    'stats': agg
                }
            )
            compute_aggs_tasks.append(compute_task)
    
    end_task = EmptyOperator(task_id = 'end_task')
    start_task >> fetch_postgres_data >> [compute_kpis_group, compute_aggs_group] >> end_task


