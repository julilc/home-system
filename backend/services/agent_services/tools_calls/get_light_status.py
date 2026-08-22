from backend.database.sql.select import select_light_status

def get_light_status():
    """
    Retrieves the latest light status from the database.

    Returns:
        str: The latest light status.
    """
    light_status_values = select_light_status(top_k=3)
    if light_status_values:
        return light_status_values[0]
    else:
        return None