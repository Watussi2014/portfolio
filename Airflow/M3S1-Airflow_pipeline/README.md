# Project Description

## Author
Arnold LAURENT
Student @ [Turing College](https://www.turingcollege.com/)

## About this Project
The goal of this project is to programmatically fetch job listing data from 3 different APIs, clean them, and then ingest them into an RDBMS. The whole data pipeline process is orchestrated by Apache Airflow.

### Learning Objectives
- Practice ingesting data from multiple sources.
- Practice orchestrating jobs using Apache Airflow.
- Practice setting up and managing an RDBMS.
- Practice using Docker Compose in your development environment.

### Data Pipeline
![m3S1data_pipeline drawio](https://github.com/user-attachments/assets/2240d5b3-3992-47e8-9708-e8ac0671e65c)


## Documentation
This project uses Docker and Docker Compose to run. Make sure you have those installed before trying to run the project.

### 1. Clone the Project
Use the following command to clone the project into the folder of your choice:

```bash
git clone https://github.com/TuringCollegeSubmissions/arlaure-DE3v2.1.5.git
```

### 2. Set Up the Environment Variables
Open the docker-compose.yaml and modify the following env variables:

- `AIRFLOW_VAR_APIID`
- `AIRFLOW_VAR_APIKEY`

With your [Adzuna](https://developer.adzuna.com/) API_ID and API_KEY

- `AIRFLOW_VAR_RAPIDAPIKEY`

With your [RapidAPI](https://rapidapi.com/) API_KEY

You can also modify `AIRFLOW_CONN_POSTGRES_JOBDB` to specify a database URI to connect to. By default, it will connect to the PostgreSQL database running with the cluster that contains Airflow metadata.

### 3. Start the Airflow Cluster
Use the following command inside the project folder to start the Airflow cluster:

```bash
docker compose up
```

### 4. Browse the Webserver and Start the DAG
Once the cluster is up, you can go to **localhost:8080** and start the **download_job_data** DAG.

The default admin user created is:
- **Username**: airflow
- **Password**: airflow


## Improvements to the project
* Improve data sources quality and size.
* Streamline more the data inside the cleaning process.
