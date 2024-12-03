import os
import shutil
from datetime import datetime
from sqlalchemy import create_engine, inspect
import pandas as pd
from config import DB_URL, DB_BACKUP_FOLDER, MODEL_BACKUP_FOLDER, MODEL_FOLDER


os.makedirs("../backups/model", exist_ok=True)
os.makedirs("../backups/db", exist_ok=True)


def backup_db(timestamp: str) -> None:
    """
    Create a backup of the database and stores it inside the container
    """
    # Database backup using SQLAlchemy
    engine = create_engine(DB_URL)
    with engine.connect() as connection:
        # Get all table names
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        # Backup each table
        for table_name in table_names:
            df = pd.read_sql_table(table_name, connection)
            backup_file = f"{DB_BACKUP_FOLDER}/{table_name}_backup_{timestamp}.csv"
            df.to_csv(backup_file, index=False)

    print(f"Database backup created at {timestamp}")


def backup_models() -> None:
    """
    Create a backup of the folder storing the model files and stores it inside the container
    """
    model_folders = [
        f
        for f in os.listdir(MODEL_FOLDER)
        if os.path.isdir(os.path.join(MODEL_FOLDER, f))
    ]

    for folder in model_folders:
        source_folder = os.path.join(MODEL_FOLDER, folder)
        backup_folder_name = f"model_{folder}_backup"
        backup_folder = os.path.join(MODEL_BACKUP_FOLDER, backup_folder_name)

        # If a backup with this name already exists, add a timestamp
        if os.path.exists(backup_folder):
            continue

        shutil.copytree(source_folder, backup_folder)
        print(f"Model folder '{folder}' backed up to '{backup_folder}'")


def cleanup_old_backups(directory: str, is_db=True) -> None:
    """
    Check if the folder containing the backups contain more than 20 files. If yes, remove the oldest.

    directory: str containing the path to the directory of the backups
    is_db: bool. Flag to indicate if the folder contains bakcup of the database or not.
    """
    if is_db:
        backups = sorted([f for f in os.listdir(directory) if f.endswith(".csv")])
        while len(backups) > 20:
            old_backup = os.path.join(directory, backups.pop(0))
            os.remove(old_backup)
            print(f"Removed old backup: {old_backup}")
    else:
        backups = sorted([f for f in os.listdir(directory)])
        while len(backups) > 20:
            old_backup = os.path.join(directory, backups.pop(0))
            shutil.rmtree(old_backup)
            print(f"Removed old backup: {old_backup}")


def create_backup():
    """
    Execute backup and cleanup functions
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_db(timestamp)
    backup_models()

    # Remove old backups if exceeding 20 backups
    cleanup_old_backups(DB_BACKUP_FOLDER)
    cleanup_old_backups(MODEL_BACKUP_FOLDER, is_db=False)

if __name__ == '__main__':
    create_backup()
