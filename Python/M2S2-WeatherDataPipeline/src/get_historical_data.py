from fetch_data import get_weather_data, get_APIQuery
from constants import LIST_CITIES
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from main import insert_data
import datetime
import config


def main():
    obj_list = []
    for city in LIST_CITIES:
        query = (
            get_APIQuery(city, start_date="2024-05-01", end_date="2024-05-31")
            + "&include=days"
        )
        weather_data = [ # Selecting only the needed attributes
            {
                key: value
                for key, value in dict.items()
                if key in ["datetime", "datetimeEpoch", "temp", "conditions", "precip"]
            }
            for dict in get_weather_data(query)["days"]
        ]

        for dict in weather_data:
            dict["timestamp"] = datetime.datetime.fromtimestamp(
                dict["datetimeEpoch"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            if not dict["precip"]:
                dict["precip"] = 0.0
            weather_obj = insert_data((city, dict))
            obj_list.append(weather_obj)

    config_file = config.access_config("DATABASE")
    engine = create_engine(config.get_url(config_file))

    with Session(engine) as session:
        session.add_all(obj_list)
        session.commit()
        print("Added the data successfully")


if __name__ == "__main__":
    main()
