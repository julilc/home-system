from backend.database.sql.select import select_humidity

def get_humidity():
    """
    Retrieves the latest humidity value from the database.

    Returns:
        float: The latest humidity value.
    """
    humidity_values = select_humidity(top_k=3)
    if humidity_values:
        return humidity_values[0]
    else:
        return None

    