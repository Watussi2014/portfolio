from loguru import logger
from download_data import dl_data, ingest_to_db, check_table_exists


def main():
    temp_folder = "/opt/temp"
    postgre_uri = "postgresql+psycopg2://postgres:postgres@postgres:5432/formula1_data"
    kaggle_data = "rohanrao/formula-1-world-championship-1950-2020"

    if not check_table_exists(db_url=postgre_uri, table_name="circuits"):
        logger.info("Initializing database...")
        dl_data(data=kaggle_data, output_path=temp_folder)
        ingest_to_db(folder_path=temp_folder, db_url=postgre_uri)
    else:
        logger.info("Database already initialized")


if __name__ == "__main__":
    main()
