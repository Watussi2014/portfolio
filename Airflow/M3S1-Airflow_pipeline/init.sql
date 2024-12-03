CREATE DATABASE job_data;

-- Connect to the job_data database
\c job_data

-- Create the jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(110),
    company_name VARCHAR(50),
    url VARCHAR(500),
    job_type VARCHAR(20),
    region VARCHAR(400),
    salary_string VARCHAR(500),
    salary NUMERIC,
    publication_timestamp TIMESTAMP
);

-- Create the analytics views 

CREATE VIEW count_de_jobs AS
SELECT 
    DATE(publication_timestamp) as day,
    COUNT(*) as de_job_count
FROM jobs 
WHERE LOWER(title) LIKE '%data engineer%'
GROUP BY DATE(publication_timestamp)
ORDER BY day;

CREATE VIEW count_de_remote_jobs AS
SELECT 
    DATE(publication_timestamp) as day,
    COUNT(*) as de_job_count
FROM jobs 
WHERE LOWER(title) LIKE '%data engineer%' AND LOWER(job_type) = 'remote'
GROUP BY DATE(publication_timestamp)
ORDER BY day;

CREATE VIEW de_stats_total AS
SELECT 
    COUNT(*) AS job_count,
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary,
    AVG(salary) AS avg_salary,
    STDDEV(salary) AS stddev_salary
FROM jobs
WHERE LOWER(title) LIKE '%data engineer%'
    AND salary != 'NaN';


CREATE VIEW de_stats_days AS
SELECT 
    DATE(publication_timestamp) AS date,
    COUNT(*) AS job_count,
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary,
    AVG(salary) AS avg_salary,
    STDDEV(salary) AS stddev_salary
FROM jobs
WHERE LOWER(title) LIKE '%data engineer%'
    AND salary != 'NaN'
GROUP BY DATE(publication_timestamp)
ORDER BY date;