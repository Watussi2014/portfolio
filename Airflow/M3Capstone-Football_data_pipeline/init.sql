CREATE DATABASE football_data;

-- Connect to the formula1_data database
\c football_data

CREATE SCHEMA IF NOT EXISTS raw;
GRANT USAGE ON SCHEMA raw TO airflow;