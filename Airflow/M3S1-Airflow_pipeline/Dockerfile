FROM apache/airflow:2.10.0

COPY requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

USER root

RUN mkdir -p /opt/temp && chown airflow /opt/temp && chmod 755 /opt/temp

USER airflow