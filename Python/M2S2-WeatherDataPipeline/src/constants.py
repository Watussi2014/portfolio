import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = "config/config.ini"
API_KEY = os.environ.get('WEATHER_API_KEY') #Fetching weather API key from env variable
LIST_CITIES = ['Istanbul', 'London', 'Saint Petersburg', 'Berlin', 'Madrid', 'Kyiv', 'Rome', 'Bucharest', 'Paris', 'Minsk', 'Vienna', 'Warsaw', 'Hamburg', 'Budapest', 'Belgrade', 'Barcelona', 'Munich', 'Kharkiv', 'Milan']