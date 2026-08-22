from backend.database.sql.select import select_persons_registered

def get_persons_registered():
    """
    Retrieves the latest persons registered from the database.

    Returns:
        list: The latest persons registered.
    """
    persons_registered_values = select_persons_registered(top_k=3)
    if persons_registered_values:
        return persons_registered_values[0]
    else:
        return None