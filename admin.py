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

def create_admin(phone_number:str):
    """Changes the is_admin value for the user provided from False to True. If no such user exists, a ValueError"""
    connection = event_db.open_connection()
    cur = connection.cursor()
    try:
        cur.execute(f"UPDATE users SET is_admin = TRUE WHERE phone_number = '{phone_number}';")
        return (f"{phone_number} now has admin priviledges.")
    except TypeError:
        return None

print(create_admin('8883331234'))