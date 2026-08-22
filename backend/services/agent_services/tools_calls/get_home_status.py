from backend.database.sql.select import select_home_status

def get_home_status():
    """
    Retrieves the latest home status from the database.

    Returns:
        str: The latest home status.
    """
    home_status_values = select_home_status(top_k=3)
    if home_status_values:
        return home_status_values[0]
    else:
        return None