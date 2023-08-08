import pyodbc
import os
from dotenv import load_dotenv
from typing import Union

# Check if the file exists
if os.path.exists("expenses/.env"):
    load_dotenv(dotenv_path="expenses/.env")


def get_cursor() -> Union[pyodbc.Cursor, None]:
    """
    This function creates a connection to the database.

    Returns
    -------
    pyodbc.Connection
        The connection to the database.
    """
    try:
        # Establish the connection
        conn = pyodbc.connect(
            f"""DRIVER=ODBC Driver 18 for SQL Server;\
            SERVER={os.getenv("SERVER")};\
            DATABASE={os.getenv("DATABASE")};\
            UID={os.getenv("USERNAME")};\
            PWD={os.getenv("PASSWORD")}"""
        )
        cursor = conn.cursor()
        return cursor
    except Exception:
        return None
