import os

DB_USERNAME = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "example")
DB_NAME = os.getenv("POSTGRES_DB", "db_metals")
DB_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@db:5432/{DB_NAME}"
MODEL_FOLDER = "/app/trained_model"
MODEL_BACKUP_FOLDER = "/app/backups/model"
DB_BACKUP_FOLDER = "/app/backups/db"
