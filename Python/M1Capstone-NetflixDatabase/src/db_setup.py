import configparser
import sqlalchemy
import os
import maskpass
import rich.progress
import subprocess
import pandas as pd
from . import constants
from . import data_transformation


os.chdir(constants.PARENT_DIR)  # Get the correct current working directory


def access_config(section: str) -> configparser.ConfigParser:
    """
    Create readable config object in the correction section.
    """
    config = configparser.ConfigParser()
    config.read(constants.CONFIG_PATH)
    current_config = config[f"{section}"]

    return current_config


class DbManager:
    """
    Object that will help with the creation and administration of a postgresql database.

    To initialize the object, you need to put a configParser object that will read the content of the config.ini file.
    """

    def __init__(self, username, pwd, server_url, port, db_name):
        self.user = username
        self.password = pwd
        self.server_url = server_url
        self.port = port
        self.db_name = db_name

        self.postgre_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.server_url}:{self.port}"
        self.db_url = self.postgre_url + f"/{self.db_name}"

        self.engine = sqlalchemy.create_engine(self.db_url)
        self.connection = self.get_connect(self.engine)


    def get_connect(self, engine) -> sqlalchemy.Connection:
        """
        Return a sqlalchemy connection object for the given engine
        """

        connect = engine.raw_connection()
        connect.set_isolation_level(0)
        return connect

    def execute_sql(self, statement: str) -> None:
        """
        Execute a SQL statement to the connection.

        connection: sqlalchemy object to connect to the database.
        statement: SQL query to be executed.
        """

        self.connection.cursor().execute(statement)
        self.connection.cursor().close()
        self.connection.commit()

    def db_exist(self, db_name: str) -> bool:
        """
        Attempt to connect to the specified database.
        Return True if the db exist, False otherwise
        """
        url = self.postgre_url + f"/{db_name}"
        engine = sqlalchemy.create_engine(url)
        try:
            engine.connect()
            return True
        except:
            return False

    def init_db(self, db_name: str) -> None:
        """
        Create the table inside the database based on the schema inside the 'create_db.sql' file
        """

        with open("src/SQL/create_db.sql", "r") as file:
            sql_statement = file.read()

        sql_statement = sql_statement.replace("$db_name$", db_name)
        sql_statement = sql_statement.replace("$db_user$", self.user)
        self.execute_sql(sql_statement)

        print("Database created")

    def init_table(self) -> None:
        """
        Create the table inside the database based on the schema inside the 'create_tables.sql' file.
        """

        with open("src/SQL/create_tables.sql", "r") as file:
            sql_statement = file.read()
        self.execute_sql(sql_statement)
        self.execute_sql(f"INSERT INTO db_users (username, user_type) VALUES ('{self.user}', 'admin');") #Creating admin user into db_user table

        print("Tables created")

    def drop_db(self, db_name: str) -> None:
        """
        Drop the database.
        """
        sql_statement = f"""DROP DATABASE {db_name} WITH (FORCE);"""
        self.execute_sql(sql_statement)
        print("Database dropped")

    def populate_table(self) -> None:
        """
        Take the transformed data inside the data folder and load it to the database
        """

        df_dict = data_transformation.clean_data()

        for table_name, df in rich.progress.track(df_dict.items(), description='Populating tables...'):
            df.to_sql(table_name, self.engine, if_exists="append", index=False)
            #print(f"{table_name} table populated")

        print("All tables populated")

    def create_user(self, user_type: str) -> None:
        """
        Add a new user that can access the database.
        user_type must be either 'DA' or 'DS'.
        Data analyst ar granted only SELECT privileges.
        Data scientist are granted SELECT and INSERT privileges.
        """
        if user_type == 'DA':
            print('Creating new data analyst login...')
            username = input('Username : ')
            password = maskpass.askpass()

            with open("src/SQL/create_da.sql", "r") as file:
                sql_statement = file.read()
            
            sql_statement = sql_statement.replace('$user', username)
            sql_statement = sql_statement.replace('$pwd', password)
            sql_statement = sql_statement.replace('$db_name', self.db_name)

            
            self.execute_sql(sql_statement)
            print('New DA succesfully created')

        elif user_type == 'DS':
            print('Creating new data scientist login...')
            username = input('Username : ')
            password = maskpass.askpass()

            with open("src/SQL/create_ds.sql", "r") as file:
                sql_statement = file.read()
            
            sql_statement = sql_statement.replace('$user', username)
            sql_statement = sql_statement.replace('$pwd', password)
            sql_statement = sql_statement.replace('$db_name', self.db_name)

            
            self.execute_sql(sql_statement)
            print('New DS succesfully created')
        
        else:
            raise ValueError('Incorrect user_type')

    def open_shell(self) -> None:
        """
        Open a psql shell to the connected database.
        """
        subprocess.run(['psql','-U', self.user, '-h', self.server_url,'-p', self.port, '-d', self.db_name])

    def query_db(self, sql_query: str) -> pd.DataFrame:
        """
        Query the database and return the results in Pandas dataframe.
        """
        return pd.read_sql_query(sql_query, self.engine)
    
    def insert_data(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Insert a dataframe to the given table.
        """
        df.to_sql(table_name, self.connection, if_exists='append', index=False)
        
    def get_usertype(self) -> str:
        """
        Return the user_type from the table db_user for the connected user.
        """
        query = sqlalchemy.text(f"SELECT user_type FROM db_users WHERE username = '{self.user}';")
        with self.engine.connect() as connection:
            result = connection.execute(query)

            for row in result:
                return row[0]