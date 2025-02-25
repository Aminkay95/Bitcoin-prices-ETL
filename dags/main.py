from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import json
from datetime import datetime, timedelta

# task 1 = extract data from the api

def extract_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    with open('/tmp/crypto_prices.json', 'w') as f:
        json.dump(data, f)

# task 2 = transform the data

def transform_data():
    with open('/tmp/crypto_prices.json', 'r') as f:
        data = json.load(f)
    transformed_data = [(data['bitcoin']['usd'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]

    with open('/tmp/crypto_prices.json', 'w') as f:  
        json.dump(transformed_data, f)

# task 3 = load the data into a postgres db in aiven

def load_to_postgres_db():
    with open('/tmp/crypto_prices.json', 'r') as f:  # Fixed path here
        data = json.load(f)
    
    hook = PostgresHook(postgres_conn_id='aiven_postgres')
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bitcoin_prices(
            bitcoin_price_usd FLOAT,
            date_and_time_of_price VARCHAR(50)
        );
        """
    )
    for price, timestamp in data:
        cursor.execute("""
            INSERT INTO bitcoin_prices(bitcoin_price_usd, date_and_time_of_price) 
            VALUES (%s, %s);
        """, (price, timestamp)) 

    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='Crypto_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
) as dag:
    
    task_fetch = PythonOperator(
        task_id='fetch_crypto_prices',
        python_callable=extract_crypto_prices  
    )

    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    task_load_db = PythonOperator(
        task_id='load_data_into_db',
        python_callable=load_to_postgres_db
    )

    # task order (dependencies)
    task_fetch >> task_transform >> task_load_db
