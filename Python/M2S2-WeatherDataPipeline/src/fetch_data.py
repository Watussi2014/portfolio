from urllib3 import request
import urllib.error
import json
import sys
import datetime
from concurrent import futures

import constants


def get_APIQuery(
    location: str, start_date: str = "", end_date: str = "", unit_group: str = "metric"
) -> str:
    """
    Build a query URL based on the given parameters.
    """
    baseURL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    API_key = constants.API_KEY
    content_type = "json"

    APIQuery = baseURL + location

    if len(start_date):
        APIQuery += "/" + start_date
        if len(end_date):
            APIQuery += "/" + end_date

    APIQuery += "?"

    if len(unit_group):
        APIQuery += "&unitGroup=" + unit_group

    if len(content_type):
        APIQuery += "&contentType=" + content_type

    APIQuery += "&key=" + API_key
    return APIQuery


def get_weather_data(query: str) -> json:
    """
    Query the visualcrossing API to get the weather data and return a JSON dictionary.
    """
    try:
        data = request("GET", query)
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print("Error code: ", e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print("Error code: ", e.code, ErrorInfo)
        sys.exit()

    return data.json()


def add_timestamp(data: dict) -> dict:
    """
    Add a timestamp key based on the dateTimeEpoch given.
    """
    for dict in data.values():
        dict["timestamp"] = datetime.datetime.fromtimestamp(
            dict["datetimeEpoch"]
        ).strftime("%Y-%m-%d %H:%M:%S")
    return data


def get_data_dict(city_list: list[str]) -> dict:
    """
    Build a query and fetch the weather data for each city in the city list given.
    """
    query_list = [get_APIQuery(city) for city in city_list]

    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(get_weather_data, query_list)

    weather_data = dict(zip(city_list, [i["currentConditions"] for i in res]))

    dict_data = {
        city: {
            key: 0 if data[key] is None else data[key]
            for key in ["datetime", "datetimeEpoch", "temp", "conditions", "precip"]
        }
        for city, data in weather_data.items()
    }  # Selecting only relevant info
    dict_data = add_timestamp(dict_data)
    return dict_data
