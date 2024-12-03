import requests
import os
import pandas as pd
from requests.structures import CaseInsensitiveDict
from sqlalchemy import create_engine
from datetime import datetime

db_username = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "example")
db_name = os.getenv("POSTGRES_DB", "db_metals")
engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@db:5432/{db_name}"
    )

def get_data() -> dict:
    """
    Fetch the data from the Metals API and return a dict containing the data
    """
    API_KEY = os.environ["METAL_API_KEY"]
    url = f"https://api.metals.dev/v1/latest?api_key={API_KEY}&currency=USD&unit=gram"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)

    data = resp.json()

    try:
        data["error_code"]
        print("Error : ", data["error_code"], data["error_message"])
        print(url)
    except KeyError:
        return data


def transform_raw_data(data_dict: dict) -> pd.DataFrame:
    """
    Clean the raw data dictionary by keeping only the relevant metals, price and timestamp.
    """
    # Error handling there
    ticker_dict = {
        "gold": "XAU",
        "silver": "XAG",
        "platinum": "XPT",
        "palladium": "XPD",
    }
    timestamp = data_dict["timestamps"]["metal"]
    rows = []

    for metal, price in data_dict["metals"].items():
        if metal in ticker_dict:
            rows.append(
                {
                    "ticker": ticker_dict[metal],
                    "name": metal,
                    "price_usd": price,
                    "timestamp": timestamp,
                }
            )
            df = pd.DataFrame(rows)
    return df


def load_data(df: pd.DataFrame, engine) -> None:
    """
    Ingest the data into the database
    """
    df.to_sql(name="price_table", con=engine, if_exists="append", index=False)
    print(datetime.now(), " : ", "Data ingested successfully")


def main():
    df = transform_raw_data(get_data())
    load_data(df,engine)

if __name__ == "__main__":
    main()
