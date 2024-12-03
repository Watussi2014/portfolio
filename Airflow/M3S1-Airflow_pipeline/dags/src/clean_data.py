import os
import json
import re
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from loguru import logger


temp_dir = os.path.join(os.path.dirname(os.getcwd()), "temp")


def extract_salary(salary_string: str) -> float:
    """
    Extract the salary from a given string using a regex formula.
    """
    salary_string = re.sub(r",", "", salary_string)
    pattern = r"(\d+(?:\.\d+)?)(?:\s*-\s*(\d+(?:\.\d+)?))?" #Regex formula that extract integers and decimals and numbers with -
    match = re.search(pattern, salary_string)
    if match:
        salary = float(match.group(1))
        if match.group(2):
            salary = float(match.group(2))
        return salary
    else:
        return np.nan


def clean_remotive() -> None:
    """
    Clean data from the Remotive API.
    """
    logger.info("Cleaning Remotive data...")
    file_dir = os.path.join(temp_dir, "remotive.json")

    with open(file_dir, "r") as f:
        data = json.load(f)
    job_list = data["jobs"]

    list_job_data = []

    # Select only relevant column and standarize their name
    for job in job_list:
        job_data = {
            "title": job["title"],
            "company_name": job["company_name"],
            "url": job["url"],
            "job_type": job["job_type"],
            "region": job["candidate_required_location"],
            "salary_string": job["salary"] or "No salary found",
            "salary": extract_salary(job["salary"]),
            "publication_timestamp": job["publication_date"],
        }
        list_job_data.append(job_data)
    cleaned_data = pd.DataFrame(list_job_data)
    cleaned_data.to_csv(
        os.path.join(temp_dir, "remotive_cleaned.csv"),
        sep=";",
        index=False,
        header=True,
        na_rep="",
    )
    logger.success("Remotive data cleaned successfully")


def clean_activejobs() -> None:
    """
    Clean data from the activejobs API.
    """
    logger.info("Cleaning activejobs data...")
    file_dir = os.path.join(temp_dir, "activejobs.json")

    with open(file_dir, "r") as f:
        data = json.load(f)

    list_job_data = []

    # Select only relevant column and standarize their name

    for job in data:
        # Check if the address is in the right format
        if isinstance(job["locations_raw"][0]["address"]["addressCountry"], dict):
            region = job["locations_raw"][0]["address"]["addressCountry"]["name"]
        else:
            region = job["locations_raw"][0]["address"]["addressCountry"]

        # Extract job type from list
        try:
            job_type = job["employmenttype"][0]
        except TypeError:
            job_type = "No job type found"

        # Extract salary from dict
        try:
            salary_string = "{}-{} {} per {}".format(
                job["salary_raw"]["value"]["minValue"],
                job["salary_raw"]["value"]["maxValue"],
                job["salary_raw"]["currency"],
                job["salary_raw"]["value"]["unitText"],
            )
            salary = job["salary_raw"]["value"]["maxValue"]
        except:
            salary_string = "No salary found"
            salary = np.nan

        job_data = {
            "title": job["title"],
            "company_name": job["organization"],
            "url": job["url"],
            "job_type": job_type,
            "region": region,
            "salary_string": salary_string,
            "salary": salary,
            "publication_timestamp": job["dateposted"],
        }
        list_job_data.append(job_data)
    cleaned_data = pd.DataFrame(list_job_data)
    cleaned_data.to_csv(
        os.path.join(temp_dir, "activejobs_cleaned.csv"),
        sep=";",
        index=False,
        header=True,
        na_rep="",
    )
    logger.success("Activejobs data cleaned successfully")


def clean_adzuna() -> None:
    """
    Clean data from the Adzuna API.
    """
    logger.info("Cleaning Adzuna data...")
    file_dir = os.path.join(temp_dir, "adzuna.json")

    with open(file_dir, "r") as f:
        data = json.load(f)

    job_list = data["results"]

    list_job_data = []
    # Select only relevant column and standarize their name
    for job in job_list:
        # Extract job type
        try:
            job_type = job["contract_time"]
        except KeyError:
            job_type = "No job type found"

        # Extract salary
        try:
            salary = job["salary_min"]
            salary_string = job["salary_min"]
        except KeyError:
            salary_string = "No salary found"
            salary = np.nan

        job_data = {
            "title": job["title"],
            "company_name": job["company"]["display_name"],
            "url": job["redirect_url"],
            "job_type": job_type,
            "region": "Belgium",
            "salary_string": salary_string,
            "salary": salary,
            "publication_timestamp": job["created"],
        }
        list_job_data.append(job_data)

    cleaned_data = pd.DataFrame(list_job_data)
    cleaned_data.to_csv(
        os.path.join(temp_dir, "adzuna_cleaned.csv"),
        sep=";",
        index=False,
        header=True,
        na_rep="",
    )
    logger.success("Adzuna data cleaned successfully")


def join_all_cleaned_data() -> None:
    """
    Loop through all files in the temp folder and add all the files ending in _cleaned.csv to a sql file ready to be ingested.
    """
    logger.info("Creating SQL file for ingesting all cleaned data")

    with open(os.path.join(temp_dir, "all_data_cleaned.sql"), "w") as f:
        f.write("BEGIN;\n")

        for file in os.listdir(temp_dir):
            if file.endswith("_cleaned.csv"):
                logger.debug(f"Loading file: {file}")
                df = pd.read_csv(os.path.join(temp_dir, file), sep=";")
                columns = ", ".join(df.columns)
                for index, row in df.iterrows():
                    values = ", ".join(
                        [
                            f"'{str(value).replace("'", " ")}'"
                            if value is not None
                            else "NULL"
                            for value in row
                        ]
                    )
                    f.write(f"INSERT INTO jobs ({columns}) VALUES ({values});\n")

        f.write("COMMIT;\n")

    logger.success("SQL file created successfully")


def read_file_from_temp(file_name: str) -> str:
    """
    Open the all_data_cleaned.sql file and return it as a string.
    """
    try:
        with open(os.path.join(temp_dir, file_name), "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File {file_name} not found")
