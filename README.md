# Hey there !
Welcome to my portfolio repository :) 


Inside you'll find some of my data engineering related project that I made during my time @ [Turing College](https://www.turingcollege.com/).

## 1. [AWS data pipeline](./AWS/Cloud_Data_Pipeline)

Using Terraform, I have build a AWS data pipeline that will restore a MS SQL database inside an RDS instance and automatically create analytics reports that will be stored inside an S3 bucket.
The infrastructure is automatically deployed using GitHub Actions

Technologies used :
* Terraform
* ECS
* Python
* MS SQL
* GitHub Actions

## 2. [Formula 1 data pipeline](./dbt/M3S2-Formula1_Data_Pipeline)
In this project I build a data pipeline that will get Formula 1 data, ingest it inside a RDBMS and then transform it using dbt.
This project taught me how what is the best way to model my data, how to use dbt and how to run dbt inside a docker container.

Technologies used : 
* Docker
* dbt
* Python
* PostgreSQL

## 3. [Football data pipeline blogpost](Airflow/M3Capstone-Football_data_pipeline)
I have written a blog post about the ETL process and data pipelines. Inside of it I explain how the data moved through the pipeline and explain the import steps along the way.
In this project I've learned the different types of data models and how to orchestrate a data pipeline using Airflow.

Technologies used : 
* Docker
* Airflow
* dbt
* Python
* PostgreSQL

## 4. [Rare metal price estimation](Python/M2Capstone-Metal_pipeline)
I built a data pipeline that will fetch the prices of rare metal, ingest them into a Postgres database and then pull it into a *fake* model to predict the price.
There I've learned how to schedule and run cron jobs, create scripts that'll listen a data base and run when new data are coming in.

Technologies used : 
* PostgreSQL
* Docker
* Python
* Cron

## Smaller projects

* [Dice generator](Python/M1S1-DiceGenerator) : My first project in Turing that taught me about OOP in Python.
* [Netflix movies and show pipeline](Python/M1Capstone-NetflixDatabase) : My first data pipeline.
* [Data modeling blog post](dbt/M3S2-Data_Modeling_Blogpost) : Another blog post where I dive deeper into the different type of data models.




