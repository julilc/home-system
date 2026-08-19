import sys
import os

sys.path.append(os.path.abspath("."))

from backend.database.sql.conection import get_connection_sql_server
from backend.database.sql.insert import insert_memory
import pandas as pd
def test_insert_memory():
    # Establish a connection to the SQL Server database
    conn = get_connection_sql_server()

    # Define test data
    id_user = 1
    memory = "This is a test memory."

    # Insert the memory into the database
    insert_memory(conn, id_user, memory)

    # Verify that the memory was inserted correctly
    cursor = conn.cursor()
    cursor.execute("SELECT memory FROM memories WHERE id_user = ?", (id_user,))
    result = cursor.fetchone()

    print(f"Retrieved memory: {result[0] if result else None}")

    assert result is not None, "Memory was not inserted."
    assert result[0] == memory, "Inserted memory does not match expected value."

    # Clean up: delete the test memory from the database
    # cursor.execute("DELETE FROM memories WHERE id_user = ?", (id_user,))
    # conn.commit()

    # Close the database connection
    conn.close()

test_insert_memory()