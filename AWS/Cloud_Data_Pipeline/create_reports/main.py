import pyodbc
import os
from loguru import logger
import time
import pandas as pd
import boto3
from concurrent.futures import ThreadPoolExecutor


SERVER = f"{os.getenv('DB_HOST')},1433"
DATABASE = "AdventureWorks"
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PWD")
S3_BUCKET = os.getenv("S3_BUCKET")

conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};DATABASE={DATABASE};SERVER={SERVER};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;"


def query_db(query: str, query_name: str) -> pd.DataFrame:
    """
    Fetches data from the database based on the provided query.
    """

    logger.info(f"Fetching data from database for {query_name}...")

    try:
        conn = pyodbc.connect(conn_str, autocommit=True, timeout=5)

        cursor = conn.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        df = pd.DataFrame.from_records(rows, columns=columns)
        logger.info(f"Df created for {query_name}")

        return df

    except Exception as e:
        logger.error(f"Error executing query {query_name}: {str(e)}")
        raise

    finally:
        # Ensure resources are properly closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info(f"Connection closed for {query_name}")


def write_parquet(df: pd.DataFrame, query_name: str) -> str:
    """
    Writes the DataFrame to a Parquet file and returns the file path.
    """

    temp_file = f"/tmp/{query_name}.parquet"
    df.to_parquet(temp_file, engine="fastparquet", compression="SNAPPY")
    file_size = os.path.getsize(temp_file)

    logger.info(f"Parquet file size for {query_name}: {file_size/1024/1024:.2f} MB")
    return temp_file


def process_query(query_name: str, query: str, s3: boto3.client) -> None:
    """
    Function that will be run asynchronously. It fetches data from the database, writes it to a Parquet file,
    and uploads it to S3.
    """
    try:
        df = query_db(query, query_name)
        temp_file = write_parquet(df, query_name)
        upload_to_s3(temp_file, query_name, s3)
        logger.info(f"Successfully processed {query_name}")
    except Exception as e:
        logger.error(f"Failed to process {query_name}: {str(e)}")


def upload_to_s3(temp_file: str, query_name: str, s3: boto3.client) -> None:
    """
    Uploads the Parquet file to S3.
    """
    logger.info(f"Uploading {query_name} to S3 Bucket {S3_BUCKET}...")
    try:
        ts = time.time()
        s3_file = f"{query_name}/{ts}.parquet"

        s3.upload_file(temp_file, S3_BUCKET, s3_file)
        logger.info(f"File {s3_file} uploaded to S3...")

    except Exception as e:
        logger.error(f"Error uploading {query_name} : {e}")


def load_queries() -> dict:
    """
    Loads all SQL queries from the ./queries folder and returns a dictionary.
    """
    queries = {}
    for filename in os.listdir("./queries"):
        if filename.endswith(".sql"):
            with open(f"./queries/{filename}") as f:
                query = f.read()
                queries[filename[:-4]] = query
    return queries

def main():
    s3 = boto3.client("s3")
    query_dict = load_queries()
    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_query, query_name, query, s3)
                for query_name, query in query_dict.items()
            ]
            for future in futures:
                future.result()  # Wait for all queries to complete
        logger.info("All queries processed.")
    except Exception as e:
        logger.error(f"Error processing queries: {str(e)}")

if __name__ == "__main__":
    main()