import os
import sqlalchemy

def init_db():
    db_username = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "example")
    db_name = os.getenv("POSTGRES_DB", "db_metals")
    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@localhost:5432/{db_name}"
    )

    with open("init_db.sql", "r") as file:
        sql_query = file.read()

    try:
        with engine.begin() as connection:
            # First drop the view to not cause issues if the script is ran with a db that's already initilized
            connection.execute(sqlalchemy.text("DROP VIEW IF EXISTS last_12_price"))
            connection.execute(sqlalchemy.text(sql_query))
            connection.commit()
            print("Database creation completed")

    except sqlalchemy.exc as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    init_db()