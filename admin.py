import event_db
""""This will handle all the admin related functions"""

def validate_admin(phone_number:str):
    """Takes a phone number in the form of a string and returns the specific users True or False value for is_admin.
    If the number provided is not found in the users table, returns None."""
    connection = event_db.open_connection()
    cur = connection.cursor()
    try:
        cur.execute(f"SELECT is_admin FROM users WHERE phone_number = '{phone_number}'")
        is_admin = cur.fetchone()[0]
        return is_admin
    except TypeError:
        return None


