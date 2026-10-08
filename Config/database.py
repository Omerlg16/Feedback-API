import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    connection = psycopg2.connect(
        user=os.environ.get("DB_USER"),
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        password=os.environ.get("DB_PASSWORD"),
        sslmode=os.environ.get("DB_SSLMODE", "prefer")
    )
    return connection
