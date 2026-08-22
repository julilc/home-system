from backend.database.sql.select import select_temperature

def get_temperature():
    """
    Retrieves the latest temperature value from the database.

    Returns:
        float: The latest temperature value.
    """
    temperature_values = select_temperature(top_k=3)
    if temperature_values:
        return temperature_values[0]
    else:
        return None