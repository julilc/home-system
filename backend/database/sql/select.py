import pyodbc
import json
from backend.database.sql.conection import get_connection_sql_server
def load_memory(id_user, top_k=10):

    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            role,
            content,
            reasoning_details
        FROM Memories
        WHERE id_user = ?
        ORDER BY created_at ASC
    """, top_k, id_user)

    rows = cursor.fetchall()

    messages = []

    for row in rows:

        message = {
            "role": row.role,
            "content": row.content
        }

        if row.reasoning_details:
            message["reasoning_details"] = json.loads(
                row.reasoning_details
            )

        messages.append(message)

    cursor.close()
    conn.close()

    return messages