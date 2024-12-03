# Project description

## Author
Arnold LAURENT
Student @ [Turing College](https://www.turingcollege.com/)

## About this project

The goal of this project is to fetch the price of rare metals (Gold, Silver, etc..) every hours and ingest this data into an RDBMS.
Every time some new data is added to the database, a script must pull the data from the last 12 entries and use it with a python script containing a model to predict the futur prices of the metals.
Lastly, the database and the model predictions must be backed up every 6 hours using a python script.



The full description of the task can be found in the file  241.ipynb

## Data ETL diagram

![metal-data-etl](https://github.com/user-attachments/assets/4db320a3-9b27-44a1-81d0-cdc0f635f885)


## Technology used in the project

* PostgreSQL
* Docker
* Python
* Git
* Cron

# How to use

Because this project use docker images available on [DockerHub](https://hub.docker.com/repositories/watussi) to accomplish the task, the project can be simply run by cloning the compose.yaml file, creating a .env file and run

````
docker-compose -f compose.yaml up
````

## .env file
The .env file shall contain those environment variables :

**POSTGRES_USER** = your_postgres_username



**POSTGRES_PASSWORD** = your_postgres_password 



**POSTGRES_DB** = name_of_the_database




**METAL_API_KEY** = [metal.dev_api_key](https://metals.dev/)

# Improvements to the project.
* The data backup script could be in another container
