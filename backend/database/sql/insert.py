import pyodbc
import json
from backend.database.sql.conection import get_connection_sql_server


def save_message(id_user, message):

    conn = get_connection_sql_server()
    cursor = conn.cursor()

    reasoning_details = message.get("reasoning_details", {})

    reasoning_details = json.dumps(
        reasoning_details,
        ensure_ascii=False
    )

    cursor.execute("""
        INSERT INTO Memories
        (
            id_user,
            role,
            content,
            reasoning_details
        )
        VALUES (?, ?, ?, ?)
    """,
        id_user,
        message.get("role"),
        message.get("content"),
        reasoning_details
    )

    conn.commit()

    cursor.close()
    conn.close()




