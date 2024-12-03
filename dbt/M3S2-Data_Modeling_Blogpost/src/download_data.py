import os
import pandas as pd
import sqlalchemy
from loguru import logger
import shutil
import kaggle


def check_table_exists(db_url: str, table_name: str) -> bool:
    """
    Check if a table exists in a database
    """
    engine = sqlalchemy.create_engine(db_url)
    insp = sqlalchemy.inspect(engine)
    return table_name in insp.get_table_names(schema="raw")


def clear_folder(folder_path: str) -> None:
    """
    Checks if a folder is empty, if it's not empty, remove everything from the folder
    """
    if not os.listdir(folder_path):
        return
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def dl_data(data: str, output_path: str) -> None:
    """
    Download the loan data from Kaggle
    """
    logger.info("Downloading data from kaggle")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    clear_folder(
        folder_path=output_path
    )  # Remove everything from temp_data to avoid duplicates.

    kaggle.api.authenticate()
    dataset = kaggle.api.dataset_list(search=data)[0]
    kaggle.api.dataset_download_files(dataset.ref, path=output_path, unzip=True)

    logger.success("Data downloaded successfully")


def ingest_to_db(folder_path: str, db_url: str) -> None:
    """
    Loop through a folder, put the csv files into a panda dataframe and then use .to_csv to ingest
    those dataframe into a postgresql database
    """

    logger.info("Ingesting data to postgresql database")

    engine = sqlalchemy.create_engine(db_url)
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, encoding = "ISO-8859-1")
            df.to_sql(
                filename.replace(".csv", ""),
                con=engine,
                schema="raw",
                if_exists="replace",
                index=False,
            )

    logger.success("Data ingested successfully")
