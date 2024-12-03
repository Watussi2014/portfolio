from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd
import select
import os
from datetime import datetime
import model
from config import DB_URL, MODEL_FOLDER


def main():
    # Create trained_model folders
    os.makedirs("./trained_model", exist_ok=True)

    # Create SQLAlchemy engine and session and metadata
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    metadata = MetaData()

    # Get the underlying psycopg2 connection
    connection = engine.raw_connection()
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    # Create a cursor and execute LISTEN
    cursor = connection.cursor()
    cursor.execute("LISTEN table_change;")

    def train_save_model() -> None:
        # Loading the view with the last 12h prices into a dataframe and trainging the model

        view = Table("last_12_price", metadata, autoload_with=engine)
        query = session.query(view)
        df = pd.read_sql(query.statement, session.bind)

        model_metals = model.Model(
            tickers=["XAU", "XAG", "XPT", "XPD"], y_size=0, x_size=0
        )
        model_metals.train(df)
        current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_metals.save(f"{MODEL_FOLDER}/{current_timestamp}")
        print("Model trained and saved succesfully !")

    print("Waiting for table update on channel 'table_change'")

    while True:
        session = Session()

        try:
            if select.select([connection], [], [], 5) != ([], [], []):
                connection.poll()
                while connection.notifies:
                    notify = connection.notifies.pop(0)
                    print("Table updated, ingesting latest data into the model...")
                    train_save_model()

        finally:
            session.close()


if __name__ == "__main__":
    main()
