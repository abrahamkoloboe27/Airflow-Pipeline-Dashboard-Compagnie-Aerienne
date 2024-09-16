import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os 

def fetch_table_from_postresql(table_name, conn_id='postgres_default'):
    pg_hook = PostgresHook(postgres_conn_id=conn_id)
    conn = pg_hook.get_conn()
    if table_name == "flights":
        query = f"SELECT * FROM {table_name} WHERE scheduled_arrival <= '2017-05-15' "
    elif table_name == "bookings" :
        query = f"SELECT * FROM {table_name} WHERE book_date <= '2017-05-15' LIMIT 10000 "
    else : 
        query = f"SELECT * FROM {table_name} LIMIT 10000"  
     
    df = pd.read_sql(query, conn)
    conn.close()
    # Ensure the directory exists
    output_dir = "dump"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df.to_csv(f"{output_dir}/{table_name}.csv", index=False)
    return f"dump/{table_name}.csv"