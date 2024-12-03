import json
import requests
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def write_to_file(data: dict, file_name: str) -> None:
    """
    Create a temp folder if it does not exist and write the given data to a new file inside the temp folder.
    """
    # Create a temporary folder in the parent directory if it does not exist
    temp_dir = os.path.join(os.path.dirname(os.getcwd()), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, f"{file_name}.json")
    # Write the data to a new file inside the temp folder
    with open(file_path, "w") as f:
        json.dump(data, f)
    logger.debug(f"Data written to {file_path}")


def fetch_data_from_api(url: str, header: str = "") -> dict:
    """
    Fetch data from an API URL.
    """
    # Send a GET request to the API URL
    response = requests.get(url, headers=header)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}")


def fetch_remotive() -> None:
    """
    Fetch data from the Remotive API.
    """
    logger.info("Fetching Remotive data...")
    url = "https://remotive.com/api/remote-jobs"
    data = fetch_data_from_api(url)
    if data:
        write_to_file(data, "remotive")
        logger.success("Remotive data fetched successfully")
    else:
        logger.error("Remotive data fetch failed")


def fetch_activejobs(rapid_api_key: str) -> None:
    """
    Fetch data from the Active Jobs API.
    """
    logger.info("Fetching Active Jobs data...")
    url = "https://active-jobs-db.p.rapidapi.com/active-ats"
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "active-jobs-db.p.rapidapi.com",
    }
    data = fetch_data_from_api(url, headers)
    if data:
        write_to_file(data, "activejobs")
        logger.success("Active Jobs data fetched successfully")
    else:
        logger.error("Active Jobs data fetch failed")


def fetch_adzuna(API_ID: str, API_KEY: str) -> None:
    """
    Fetch data from the Adzuna API.
    """
    logger.info("Fetching Adzuna data...")
    url = f"https://api.adzuna.com/v1/api/jobs/be/search/1?app_id={API_ID}&app_key={API_KEY}&results_per_page=100"
    data = fetch_data_from_api(url)
    if data:
        write_to_file(data, "adzuna")
        logger.success("Adzuna data fetched successfully")
    else:
        logger.error("Adzuna data fetch failed")
