import pandas as pd
import os
from ast import literal_eval


# Setting the cwd correctly
main_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_dir)
PATH = os.path.join("data")


def clean_titles(raw_titles_df: pd.DataFrame) -> tuple:
    """
    Perform the data transformation needed on the raw_titles dataframe
    """
    # Removing nan
    raw_titles_df = raw_titles_df.dropna(subset=["title"])
    # Splitting the genres column
    genres_df = pd.DataFrame()
    raw_titles_df.loc[:,"genres"] = raw_titles_df["genres"].apply(
        literal_eval
    ) # Transforming the list into a correct format.
    genres_df[["id", "genres"]] = raw_titles_df[["id", "genres"]].explode(
        column="genres"
    )
    raw_titles_df = raw_titles_df.drop(
        columns="genres"
    )  # Dropping the column because the data is in another dataframe.

    # Splitting the production countries column
    production_df = pd.DataFrame()
    raw_titles_df["production_countries"] = raw_titles_df["production_countries"].apply(
        literal_eval
    )  # Transforming the list into a correct format.
    production_df[["id", "production_countries"]] = raw_titles_df[
        ["id", "production_countries"]
    ].explode(column="production_countries")
    raw_titles_df = raw_titles_df.drop(columns="production_countries")

    # Removing index column
    raw_titles_df = raw_titles_df.drop(columns="index")

    return (raw_titles_df, genres_df, production_df)


def add_id(df: pd.DataFrame, raw_title: pd.DataFrame) -> pd.DataFrame:
    """
    Join a data frame on 'title' column to raw_title dataframe and add the 'id' column.
    """
    df = df.drop(columns="index")
    col = list(df.columns)
    col.insert(0, "id")
    df = df.merge(raw_title, left_on="TITLE", right_on="title", how="left")

    return df[col]


def clean_data() -> dict:
    """
    Perform the data cleaning process and return a dictionary with the dataframes cleaned.
    """
    cleaned_df = {}

    raw_titles_df = pd.read_csv(os.path.join(PATH, "raw_titles.csv"))
    raw_credits_df = pd.read_csv(os.path.join(PATH, "raw_credits.csv"))
    best_movies_df = pd.read_csv(os.path.join(PATH, "Best Movies Netflix.csv"))
    best_movie_years_df = pd.read_csv(
        os.path.join(PATH, "Best Movie by Year Netflix.csv")
    )
    best_shows_df = pd.read_csv(os.path.join(PATH, "Best Shows Netflix.csv"))
    best_show_years_df = pd.read_csv(
        os.path.join(PATH, "Best Show by Year Netflix.csv")
    )

    # Applying clean_titles function and adding the returning df to the cleaned_df dict
    tup = clean_titles(raw_titles_df)
    cleaned_df["titles"] = tup[0]
    cleaned_df["genres"] = tup[1]["genres"].drop_duplicates().dropna()
    cleaned_df["movie_genre"] = tup[1]
    cleaned_df["production_countries"] = (
        tup[2]["production_countries"].drop_duplicates().dropna()
    )
    cleaned_df["movie_production"] = tup[2]

    # raw_credits df just need the index column removed
    raw_credits_df = raw_credits_df.drop(columns="index")
    raw_credits_df = raw_credits_df[
        raw_credits_df["id"] != "tm1063792"
    ]  # removing movie with no title
    cleaned_df["credits"] = raw_credits_df

    # Removing index column and adding id column.
    best_movies_df = add_id(best_movies_df, raw_titles_df)
    best_movie_years_df = add_id(best_movie_years_df, raw_titles_df)
    best_shows_df = add_id(best_shows_df, raw_titles_df)
    best_show_years_df = add_id(best_show_years_df, raw_titles_df)

    cleaned_df["best_movies"] = best_movies_df[["id", "MAIN_GENRE", "MAIN_PRODUCTION"]]
    cleaned_df["best_movie_year"] = best_movie_years_df[["id", "RELEASE_YEAR"]]
    cleaned_df["best_shows"] = best_shows_df[["id", "MAIN_GENRE", "MAIN_PRODUCTION"]]
    cleaned_df["best_shows_year"] = best_show_years_df[["id", "RELEASE_YEAR"]]

    return cleaned_df
