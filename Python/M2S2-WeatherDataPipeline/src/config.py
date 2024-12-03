import os
import configparser
import constants


os.chdir(constants.PARENT_DIR)  # Get the correct current working directory


def access_config(section: str) -> configparser.ConfigParser:
    """
    Create readable config object in the correction section.
    """
    config = configparser.ConfigParser()
    config.read(constants.CONFIG_PATH)
    current_config = config[f"{section}"]

    return current_config

def get_url (config: configparser.ConfigParser) -> str:
    """
    Fetch the database config data and return a url to be passed into a SQLAlchemy engine.
    """
    username = os.environ.get('DB_USERNAME')
    pwd = os.environ.get('DB_PASSWORD')
    if not username:
        raise ValueError("Can't fetch correct username, check if your env variable 'DB_USERNAME' is set correctly")
    if not pwd:
        raise ValueError("Can't fetch correct password, check if your env variable 'DB_PASSWORD' is set correctly")
    return f"postgresql+psycopg2://{username}:{pwd}@{config['server_url']}:{config['port']}/{config['db_name']}"