from backend.database.sql.select import select_luminosity

def get_luminosity():
    """
    Retrieves the latest luminosity value from the database.

    Returns:
        float: The latest luminosity value.
    """
    luminosity_values = select_luminosity(top_k=3)
    if luminosity_values:
        return luminosity_values[0]
    else:
        return None

