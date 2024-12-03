# Description

This project aims to collect weather data from the top 20 cities in Europe every hours and generate analytics KPI for them.


# Project plan

1. Create script that will fetch the weather data and ingest them to an RDBMS.

2. Setup a cron job that will collect new data every hours.

3. Provide views with analytics functions.

4. Build the benchmark that will compare the speed for fetching the data between different asynchronous programing methods.


# Running the project

## 1. Install the requirements

````
pip install -r requirements.txt
````


## 2. Setup the configuration file and environements variables

Change the config.ini file to setup the database connection.

You also need to set up the env variable DB_USERNAME and DB_PASSWORD

The API where the data is fetched is from [VisualCrossing](https://www.visualcrossing.com/weather-data). You need to create an account and setup the env variable WEATHER_API_KEY with your API key.


## 3. Running the python script

There are 2 main script in the project :

1. **get_historical_data.py** : This script will fetch the data for the full month of May and ingest it into the database. This script is designed to be run only once.

2. **main.py** : This script will fetch the weather for the last hour and ingest it to the database. The script is designed to be run periodically via a cron job.


# Data analytics

After you have collected some data, you can use the query inside *src/sql* directory to create some views that will return analytics KPI. For example, the maximum, minimum, and standard deviation of temperatures.

# Improvements for the project

* Letting the user chose the range of date for the historical data
* More analytics KPI