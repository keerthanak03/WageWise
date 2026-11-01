import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def test_db_connection():
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()

        return {
            "status": "connected",
            "database": "WageWise",
            "version": result[0]
        }

    except Exception as error:
        return {
            "status": "failed",
            "error": str(error)
        }