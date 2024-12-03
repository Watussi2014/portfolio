from sqlalchemy import create_engine, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session
from concurrent import futures
import config
import fetch_data
import constants

class Base (DeclarativeBase):
    pass

class WeatherData (Base):

    __tablename__ = 'weather_data'

    city = mapped_column(String(50), primary_key=True)
    timestamp = mapped_column(DateTime, primary_key=True)
    temp = mapped_column(Float)
    precip = mapped_column(Float)
    conditions = mapped_column(String)

    def __repr__(self) -> str:
        return f"WeatherData(city={self.city!r}, timestamp={self.timestamp!r}, temp={self.temp!r}, precip={self.precip!r}, conditions={self.conditions!r})"

def insert_data(tup: tuple) -> WeatherData:
    """
    Insert the data from the data dictionnary into a WeatherData object.
    """
    city = tup[0]
    data = tup[1]
    return WeatherData(city=city, timestamp=data['timestamp'], temp=data['temp'], precip=data['precip'], conditions=data['conditions'])

def main ():
    config_file = config.access_config('DATABASE')
    engine = create_engine(config.get_url(config_file))
    cities = constants.LIST_CITIES
    data_dict = fetch_data.get_data_dict(cities)

    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(insert_data, ((city, data) for city, data in data_dict.items()))
    
    obj_list = [weather_obj for weather_obj in res]

    with Session(engine) as session:
        session.add_all(obj_list)
        session.commit()
        print('Added the data successfully')

if __name__ == "__main__":
    main()