from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
import src.get_data as get_data
import src.clean_data as clean_data

dag = DAG(
    dag_id="download_job_data",
    schedule_interval=None,
)

fetch_remotive = PythonOperator(
    task_id="fetch_remotive", 
    python_callable=get_data.fetch_remotive, 
    dag=dag
)

fetch_adzuna = PythonOperator(
    task_id="fetch_adzuna",
    python_callable=get_data.fetch_adzuna,
    op_kwargs={"API_ID": Variable.get("apiid"), "API_KEY": Variable.get("apikey")},
    dag=dag,
)

fetch_activejobs = PythonOperator(
    task_id="fetch_activejobs",
    python_callable=get_data.fetch_activejobs,
    op_kwargs={"rapid_api_key": Variable.get("rapidapikey")},
    dag=dag,
)

clean_remotive = PythonOperator(
    task_id="clean_remotive", 
    python_callable=clean_data.clean_remotive, 
    dag=dag
)

clean_adzuna = PythonOperator(
    task_id="clean_adzuna", 
    python_callable=clean_data.clean_adzuna, 
    dag=dag
)

clean_activejobs = PythonOperator(
    task_id="clean_activejobs", 
    python_callable=clean_data.clean_activejobs, 
    dag=dag
)

join_all_cleaned_data = PythonOperator(
    task_id="join_all_cleaned_data",
    python_callable=clean_data.join_all_cleaned_data,
    dag=dag,
)

ingest_data = PostgresOperator(
    task_id="ingest_data",
    sql=clean_data.read_file_from_temp("all_data_cleaned.sql"),
    postgres_conn_id="postgres_jobdb",
    dag=dag,
)


fetch_remotive >> clean_remotive
fetch_adzuna >> clean_adzuna
fetch_activejobs >> clean_activejobs
[clean_remotive, clean_adzuna, clean_activejobs] >> join_all_cleaned_data
join_all_cleaned_data >> ingest_data
