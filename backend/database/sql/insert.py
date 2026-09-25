import pyodbc
import json
from backend.database.sql.conection import get_connection_sql_server


def save_message(id_user, message, model):

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
            reasoning_details,
            model
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        id_user,
        message.get("role"),
        message.get("content"),
        reasoning_details,
        model
    )

    conn.commit()

    cursor.close()
    conn.close()




def insert_temperature(id_device, temperature):
    """
    Inserts a temperature reading into the database.

    Args:
        id_device (str): The ID of the sensor.
        temperature (float): The temperature value to insert.
    """
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Temperature
        (
            id_device,
            temperature,
            created_at
        )
        VALUES (?, ?, GETDATE())
    """,
        id_device,
        temperature
    )

    conn.commit()

    cursor.close()
    conn.close()

def insert_humidity(id_device, humidity):
    """
    Inserts a humidity reading into the database.

    Args:
        id_device (str): The ID of the sensor.
        humidity (float): The humidity value to insert.
    """
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Humidity
        (
            id_device,
            humidity,
            created_at
        )
        VALUES (?, ?, GETDATE())
    """,
        id_device,
        humidity
    )

    conn.commit()

    cursor.close()
    conn.close()

def insert_luminosity(id_device, luminosity):
    """
    Inserts a luminosity reading into the database.

    Args:
        id_device (str): The ID of the sensor.
        luminosity (float): The luminosity value to insert.
    """
    conn = get_connection_sql_server()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Luminosity
        (
            id_device,
            luminosity,
            created_at
        )
        VALUES (?, ?, GETDATE())
    """,
        id_device,
        luminosity
    )

    conn.commit()

    cursor.close()
    conn.close()