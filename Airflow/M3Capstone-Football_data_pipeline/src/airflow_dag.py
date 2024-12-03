from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from dotenv import load_dotenv
import datetime
import get_data
import insert_data
import os

load_dotenv()
competitions = ['PL', 'CL', 'BL1', 'SA', 'PD']

dag = DAG(
    dag_id="download_football_data",
    schedule_interval="0 0 * * 1",
    start_date=datetime.datetime(2024, 8, 10), #Start of the earliest competition
    catchup=True
)

fetch_data = PythonOperator(
    task_id="fetch_data",
    python_callable=get_data.fetch_all_competitions,
    op_kwargs={"competitions": competitions, 
               "execution_date": "{{ds}}"},
    dag=dag
)

upload_data = PythonOperator(
    task_id="upload_data",
    python_callable=insert_data.upload_data,
    op_kwargs={"db_url": os.getenv('DBURL')},
    dag=dag
)

remove_data = PythonOperator(
    task_id="remove_data",
    python_callable=insert_data.remove_data,
    dag=dag
)

run_dbt = BashOperator(
    task_id="run_dbt",
    bash_command="dbt build --project-dir /opt/airflow/dbt_football --profiles-dir /.dbt",
    dag=dag
)

fetch_data >> upload_data >> remove_data >> run_dbt
