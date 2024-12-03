import os
import sys
import configparser
from . import constants

os.chdir(constants.PARENT_DIR)


def config_exist() -> bool:
    return os.path.exists(constants.CONFIG_PATH)


def argv_exist() -> bool:
    return len(sys.argv) == 4


def get_config() -> None:
    """
    Check if the config.ini file already exist or argv are given.
    If not, prompt the user for the database information and write it to a new config.ini file
    """
    if config_exist() == True:
        print("Config file loaded correctly")
        return None

    elif argv_exist() == True:
        server_url = sys.argv[1]
        port = sys.argv[2]
        db_name = sys.argv[3]

    else:
        print("No config given, prompting now ...")
        server_url = input("What is the server url to the database : ")
        port = input("What is the port for the database : ")
        db_name = input("What is the database name : ")

    config = configparser.ConfigParser()
    config["DATABASE"] = {
        "server_url": server_url,
        "port": port,
        "db_name": db_name,
    }

    with open(constants.CONFIG_PATH, "w") as configfile:
        config.write(configfile)

    print("Config file loaded correctly")
