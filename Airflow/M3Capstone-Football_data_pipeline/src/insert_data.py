import pandas as pd
import json
import os
from loguru import logger
import sqlalchemy


def read_json(json_file: str) -> pd.DataFrame:
    """
    Reads a JSON file and creates a pandas DataFrame with the specified columns.
    
    Args:
        json_file (str): Path to the JSON file to read.
    """
    # Specify the desired column names
    columns = [
        'id',
        'competition_name',
        'utc_date',
        'matchday',
        'stage',
        'home_team_name',
        'home_team_tla',
        'away_team_name',
        'away_team_tla',
        'winner',
        'duration',
        'home_team_score',
        'away_team_score'
    ]
    
    # Read the JSON file and create the DataFrame
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract the relevant data from the JSON and create the DataFrame
    matches = []
    for match in data['matches']:
        match_data = {
            'id': match['id'],
            'competition_name': data['competition']['name'],
            'utc_date': match['utcDate'],
            'matchday': match['matchday'],
            'stage': match['stage'],
            'home_team_name': match['homeTeam']['name'],
            'home_team_tla': match['homeTeam']['tla'],
            'away_team_name': match['awayTeam']['name'],
            'away_team_tla': match['awayTeam']['tla'],
            'winner': match['score']['winner'],
            'duration': match['score']['duration'],
            'home_team_score': match['score']['fullTime']['home'],
            'away_team_score': match['score']['fullTime']['away']
        }
        matches.append(match_data)
    
    return pd.DataFrame(matches, columns=columns)


def read_all_files(directory: str = '/opt/temp/') -> pd.DataFrame:
    """
    Reads all JSON files in the specified directory and returns a single pandas DataFrame.
    
    Args:
        directory (str): The directory containing the JSON files (default is '../last_data').
        
    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from all JSON files.
    """
    dfs = []
    
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
            df = read_json(file_path)
            dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    return pd.concat(dfs, ignore_index=True)


def upload_data(db_url: str) -> None:

    """
    Uploads data from all JSON files in the /opt/temp/ directory to the specified database.
    
    Args:
        db_url (str): The URL of the database to upload to.
    """
    logger.info(f"Uploading data to database with url: {db_url}")

    df = read_all_files()
    engine = sqlalchemy.create_engine(db_url)
    df.to_sql('matches_data', con=engine, if_exists='append', index=False, schema='raw')
    logger.success("Data uploaded successfully")

def remove_data() -> None:
    """
    Removes all JSON files from the /opt/temp/ folder.
    """
    for filename in os.listdir('/opt/temp/'):
        if filename.endswith('.json'):
            file_path = os.path.join('/opt/temp/', filename)
            os.remove(file_path)
            logger.info(f"Removed {filename}")
