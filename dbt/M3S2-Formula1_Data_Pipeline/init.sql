CREATE DATABASE formula1_data;

-- Connect to the formula1_data database
\c formula1_data

CREATE SCHEMA IF NOT EXISTS raw;
GRANT USAGE ON SCHEMA raw TO postgres;

CREATE SCHEMA IF NOT EXISTS target;
GRANT USAGE ON SCHEMA target TO postgres;