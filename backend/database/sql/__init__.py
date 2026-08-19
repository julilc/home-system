

def insert_memory(conn, id_user, memory)-> None:
    """
    Inserts a memory into the database.

    Args:
        conn: The database connection object.
        id_user: The ID of the user.
        memory: The memory to be inserted.

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memories (id_user, memory) VALUES (?, ?)",
        (id_user, memory)
    )
    conn.commit()
