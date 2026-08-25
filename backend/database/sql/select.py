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
        ORDER BY created_at DESC
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

def select_temperature(top_k=1):
    """
    Selects the temperature value from the database.

    Args:
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?) *
        FROM vw_Temperature
        ORDER BY created_at DESC
    """, top_k)

    rows = cursor.fetchall()

    temperatures = [
        {
            "created_at": row.created_at.isoformat(),
            "id_device": row.id_device,
            "temperature": row.temperature
        }
        for row in rows
    ]


    cursor.close()
    conn.close()

    return temperatures

def select_humidity(top_k=1):
    """
    Selects the humidity value from the database.

    Args:
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            humidity
        FROM vw_Humidity
        ORDER BY created_at DESC
    """, top_k)

    rows = cursor.fetchall()

    humidities = [row.humidity for row in rows]

    cursor.close()
    conn.close()

    return humidities

def select_light_status(room, top_k=1):
    """
    Selects the light status for a specific room from the database.

    Args:
        room (str): The name of the room.
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            status
        FROM vw_LightStatus
        WHERE room = ?
        ORDER BY created_at DESC
    """, top_k, room)

    rows = cursor.fetchall()

    light_statuses = [row.status for row in rows]

    cursor.close()
    conn.close()

    return light_statuses

def select_music_played(top_k=1):
    """
    Selects the music played from the database.

    Args:
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            song
        FROM vw_MusicPlayed
        ORDER BY created_at DESC
    """, top_k)

    rows = cursor.fetchall()

    songs_played = [row.song for row in rows]

    cursor.close()
    conn.close()

    return songs_played

def select_persons_registered(top_k=1):
    """
    Selects the persons registered on the front door from the database.

    Args:
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            person_name
        FROM vw_PersonsRegistered
        ORDER BY created_at DESC
    """, top_k)

    rows = cursor.fetchall()

    persons_registered = [row.person_name for row in rows]

    cursor.close()
    conn.close()

    return persons_registered


def select_home_status(top_k=1):
    """
    Selects the home status from the database.

    Args:
        top_k (int): The number of latest records to retrieve. Default is 1.
    """
    
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?)
            status
        FROM vw_HomeStatus
        ORDER BY created_at DESC
    """, top_k)

    rows = cursor.fetchall()

    home_statuses = [row.status for row in rows]

    cursor.close()
    conn.close()

    return home_statuses