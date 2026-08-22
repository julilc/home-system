from backend.database.sql.select import select_music_played

def get_music_played():
    """
    Retrieves the latest music played from the database.

    Returns:
        str: The latest music played.
    """
    music_played_values = select_music_played(top_k=3)
    if music_played_values:
        return music_played_values[0]
    else:
        return None
    