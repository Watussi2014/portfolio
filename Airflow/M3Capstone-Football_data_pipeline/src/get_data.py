import os
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from loguru import logger
from typing import List, Dict
from dotenv import load_dotenv
from utils import is_not_future_date, write_json_to_file

load_dotenv()

async def fetch_competition_results(session: aiohttp.ClientSession, 
                                 competition: str, 
                                 start_date: str, 
                                 end_date: str) -> json:
    """
    Asynchronously fetches results for a single competition.
    
    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for requests
        competition (str): The competition ID
        start_date (str): Start date in yyyy-MM-dd format
        end_date (str): End date in yyyy-MM-dd format
    """

    if not (is_not_future_date(start_date) and is_not_future_date(end_date)):
        raise ValueError('Start date and end date must not be in the future')

    uri = f'https://api.football-data.org/v4/competitions/{competition}/matches'
    params = {
        'status': 'FINISHED',
        'dateFrom': start_date,
        'dateTo': end_date
    }
    headers = { 'X-Auth-Token': os.getenv("APIKEY") }

    #try:
    async with session.get(uri, params=params, headers=headers) as response:
        if response.status == 200:
            logger.info(f"Fetched results for {competition}")
            return await response.json()
        else:
            raise Exception(f"Error fetching competition {competition}: {response.status}")



async def get_multiple_competition_results(competitions: List[str], 
                                        start_date: str, 
                                        end_date: str) -> List[Dict]:
    """
    Asynchronously fetches results for multiple competitions.
    
    Args:
        competitions (List[str]): List of competition IDs
        start_date (str): Start date in yyyy-MM-dd format
        end_date (str): End date in yyyy-MM-dd format
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for competition in competitions:
            task = fetch_competition_results(session, competition, start_date, end_date)
            tasks.append(task)
        
        # Gather all tasks and wait for them to complete
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

def fetch_all_competitions(competitions: List[str], 
                         execution_date: str) -> List[Dict]:
    """
    Wrapper function to run the async code in asynchronous context.
    """
    end_date = datetime.strptime(execution_date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=6)

    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')

    logger.info(f"Fetching data for {len(competitions)} competitions")

    json_data = asyncio.run(
        get_multiple_competition_results(competitions, start_date, end_date)
    )
    logger.success("Data fetched successfully")
    logger.info("Writing data to JSON file")
    for dict in json_data:
        filename =write_json_to_file(dict)
        logger.success(f"Data written to {filename}")




     
