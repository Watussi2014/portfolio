# 1. Goals of the project
This project aims at creating, populating and accessing a PostegreSQL database using python and its libraries.

The database can be accessed either via the python script or via an API by importing the python files and creating your own DbManager object.

# 2. Project plan

1. **Extract the data**   
The data is from [kaggle](https://www.kaggle.com/datasets/thedevastator/the-ultimate-netflix-tv-shows-and-movies-dataset/data). Download the csv files and put them inside our project folder.

2. **Transform the data**   
Open the csv files, check if the data is formated correctly and apply the needed transformation so that the data is ready to be uploaded to a RDBMS.

3. **Load the data**   
Setup the RDBMS, create the schema for the database and upload the data to the database.

4. **Create the API**   
Create the API to read and write to the database from Python.

5. **Create documentation**    
Update the README and create docstrings to explain the code.

# 3. Data transformation

I have made two files for the data transformation step :

1. **data_transformation.ipynb**
A Jupyter notebook where I explain the process behind the cleaning of each csv file.

2. **src/data_transformation.py**
A python script where I do the actual transformation and create a list with the cleaned dataframe ready to be ingested into the database.


# 4. How to use

1) Download the [csv files](https://www.kaggle.com/datasets/thedevastator/the-ultimate-netflix-tv-shows-and-movies-dataset/data) and put them into the data folder.

2) Install the dependecies for the project using :

    ````
    pip install -r requirements.txt
    ````

3) Setup the config file to connect to the database.    
    Either create a config.ini following the config_example.ini format.    
    OR     
    Launch the script with those arguments :
    ```
    python main.py server_url port db_name
    ```     
    OR      
    If none of those steps are made, you'll be prompted your database information on the first launch of the script.

4) Run main.py. You'll be prompted your login informations to connect to the database. 

Afterward, the database will be created and populated and you'll be able to create new users with either READ only rights or READ and WRITE rights.


# 5. Accessing the API

If you wish to create a DbManager object, you need to pass it 5 arguments :     

* Your username to access the server
* The password of your account
* The server url
* The port
* The database name you wish to connect to

```
db = DbManager(username, password, server_url, port, db_name)
```

The 3 mains method to interact with the database are :     

## .open_shell()

````
DbManager.open_shell() -> None
````

Will open psql shell directly connected to the database.

## .query_db()

````
DbManager.query_db(sql_query) -> pandas.Dataframe
````

Send a query to the database and return the result.    

The argument **sql_query** must be a string with your query inside.    
The function returns a pandas dataframe with the results of the query.

## .insert_data()

```
DbManager.insert_data(table_name, dataframe) -> None
```

Insert a dataframe into a specific table.

The argument are **table_name**, a string with the name of table where you wish to insert the data and **dataframe**, a pandas Dataframe containing the data you wish to append to the table.


# 6. Improvements for the project

* Being able to create more type of users with differents permissions.

* Provide more advanced API with functionalities such as : creating new tables, updating or deleting data, changing the settings of the tables.
