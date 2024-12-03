# Project Description

## Author
Arnold LAURENT
Student @ [Turing College](https://www.turingcollege.com/)

## About this Project
The goal of this project is to fetch formula 1 data from [Kaggle](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/), ingest it to an RDBMS and then transform it using dbt.

### Learning Objectives
- Practice ingesting data to an RDBMS.
- Practice using dbt.
- Practice using dimensional data modeling.
- Practice data denormalization.
- Practice using Docker Compose in your development environment.



## Documentation
This project uses Docker and Docker Compose to run. Make sure you have those installed before trying to run the project.

### 1. Clone the Project
Use the following command to clone the project into the folder of your choice:

```bash
git clone https://github.com/TuringCollegeSubmissions/arlaure-DE3v2.2.5.git
```

### 2. Set Up the Environment Variables
Create a new .env file inside the project folder and add it the following environment variables :

- KAGGLE_USERNAME=your_kaggle_username
- KAGGLE_KEY=your_kaggle_api_key

### 3. Start the docker compose cluster
Use the following command inside the project folder to start the docker cluster:

```bash
docker compose up
```

The cluster will :

1) Create and setup a PostgreSQL container.
2) Run a python script to download and ingest the data into the database.
3) Run dbt to transform the data into new models.



## Improvements to the project
* Add users and role to the database to improve security

