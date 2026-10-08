import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    connection = psycopg2.connect(
        user=os.environ.get("DB_USER"),
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        password=os.environ.get("DB_PASSWORD"),
        sslmode=os.environ.get("DB_SSLMODE", "prefer")
    )
    try:
        cursor = connection.cursor()
        cursor.execute(schema_sql)
        connection.commit()
        print("Table 'reviews' prête.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
