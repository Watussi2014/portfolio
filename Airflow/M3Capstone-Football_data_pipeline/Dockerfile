FROM apache/airflow:2.10.0

COPY ./src/airflow_dag.py ./src/get_data.py ./src/insert_data.py ./src/utils.py ./.env /opt/airflow/dags/

COPY requirements.txt /

COPY ./dbt_football /opt/airflow/dbt_football

COPY ./profiles.yml /.dbt/profiles.yml

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

USER root
RUN mkdir -p /opt/temp/ && chown airflow /opt/temp && chmod 755 /opt/temp
RUN mkdir -p /opt/airflow/dbt_football/logs && \
    chmod -R 777 /opt/airflow/dbt_football
USER airflow
