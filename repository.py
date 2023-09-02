import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
import os

conn = None
load_dotenv()


def init_db():
    global conn
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )


def close_db():
    global conn
    if conn:
        conn.close()


@contextmanager
def get_cursor():
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        conn.commit()


def init_table():
    with get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                price FLOAT NOT NULL,
                date DATE NOT NULL,
                weight FLOAT NOT NULL,
                height FLOAT NOT NULL,
                width FLOAT NOT NULL,
                depth FLOAT NOT NULL,
                manufacturer TEXT NOT NULL
            );
        """)
