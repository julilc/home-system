import pyodbc
import os

def get_connection_sql_server():
    """
    Establishes a connection to the SQL Server database.

    Returns:
        conn: The database connection object.
    """
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f"SERVER={os.getenv('SQL_DB_SERVER')};"
        f"DATABASE={os.getenv('SQL_DB_NAME')};"
        f"UID={os.getenv('SQL_DB_USER')};"
        f"PWD={os.getenv('SQL_DB_PASSWORD')};"
    )
    return conn