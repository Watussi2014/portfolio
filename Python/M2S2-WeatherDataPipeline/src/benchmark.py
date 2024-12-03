from fetch_data import get_APIQuery, get_weather_data, add_timestamp
from constants import LIST_CITIES
from concurrent import futures
from time import perf_counter
import asyncio
import aiohttp

city_list = LIST_CITIES


def fetch_seq():
    t0 = perf_counter()

    query_list = {city: get_APIQuery(city) for city in city_list}
    weather_data = {}
    for city, query in query_list.items():
        json_data = get_weather_data(query)
        weather_data[city] = json_data["currentConditions"]

    dict_data = {
        city: {
            key: data[key]
            for key in ["datetime", "datetimeEpoch", "temp", "conditions", "precip"]
        }
        for city, data in weather_data.items()
    }
    dict_data = add_timestamp(dict_data)
    total_time = perf_counter() - t0
    print(dict_data)
    print(f"Total time for sequential function : {total_time}")


def fetch_thread():
    t0 = perf_counter()
    query_list = [get_APIQuery(city) for city in city_list]

    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(get_weather_data, query_list)

    weather_data = dict(zip(city_list, [i["currentConditions"] for i in res]))

    dict_data = {
        city: {
            key: data[key]
            for key in ["datetime", "datetimeEpoch", "temp", "conditions", "precip"]
        }
        for city, data in weather_data.items()
    }
    dict_data = add_timestamp(dict_data)
    total_time = perf_counter() - t0
    print(dict_data)
    print(f"Total time for thread function : {total_time}")


async def async_weather_data(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(query) as resp:
            data = await resp.json()
            return data


async def fetch_coroutines():
    query_list = [get_APIQuery(city) for city in city_list]
    coros = [async_weather_data(query) for query in query_list]
    data_dict = {}
    for coro in asyncio.as_completed(coros):
        data = await coro
        data_dict[data["address"]] = data["currentConditions"]

    return data_dict


async def main():
    t0 = perf_counter()
    weather_data = await fetch_coroutines()
    dict_data = {
        city: {
            key: data[key]
            for key in ["datetime", "datetimeEpoch", "temp", "conditions", "precip"]
        }
        for city, data in weather_data.items()
    }
    dict_data = add_timestamp(dict_data)
    total_time = perf_counter() - t0
    print(dict_data)
    print(f"Total time for coroutine function : {total_time}")


asyncio.run(main())
fetch_thread()
fetch_seq()
