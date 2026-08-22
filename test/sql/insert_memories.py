import sys
import os

sys.path.append(os.path.abspath("."))

from backend.database.sql.conection import get_connection_sql_server
from backend.database.sql.insert import insert_memory
import pandas as pd
def test_insert_memory():
    # Create a sample DataFrame with test data
    test_data = pd.DataFrame({
        "id_user": ["test_user"],
        "role": ["user"],
        "content": ["This is a test message."],
        "reasoning_details": [None]
    })

    # Call the insert_memory function with the test data
    insert_memory(test_data)

    # Verify that the data was inserted into the database
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chat_memory WHERE id_user = 'test_user'")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    assert len(result) == 1, "Memory insertion failed."