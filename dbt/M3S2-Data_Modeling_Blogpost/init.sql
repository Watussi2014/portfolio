CREATE DATABASE bike_sale;

-- Connect to the formula1_data database
\c bike_sale

CREATE SCHEMA IF NOT EXISTS raw;
GRANT USAGE ON SCHEMA raw TO postgres;

CREATE SCHEMA IF NOT EXISTS target;
GRANT USAGE ON SCHEMA target TO postgres;