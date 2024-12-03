from sqlalchemy import text
import maskpass
from . import db_setup


def prompt_login() -> tuple:
    user = input("Username : ")
    pwd = maskpass.askpass()
    return (user, pwd)


def can_createdb(db: db_setup.DbManager) -> bool:
    """
    Check if the user connected to the database has the permissions to create new databases.
    """
    query = text(f"SELECT rolcreatedb FROM pg_roles WHERE rolname = '{db.user}';")

    with db.engine.connect() as connection:
        result = connection.execute(query)

        for row in result:
            return row[0]
