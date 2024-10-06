from abc import ABC, abstractmethod
import os
from pathlib import Path
import dotenv
import psycopg2

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")


class Database(ABC):
    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):
    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )


new_table = "new_table"


def createTable():
    with PgDatabase() as db:
        db.cursor.execute(f"""CREATE TABLE {new_table} (
            id SERIAL PRIMARY KEY,
            created_time TIMESTAMPTZ DEFAULT NOW(),
            name VARCHAR(255)
            );
        """)
        db.connection.commit()
        print("Table created successfully")


def dropTable():
    with PgDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {new_table} CASCADE;")
        db.connection.commit()
        print("Table has been dropped")
