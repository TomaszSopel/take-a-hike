import event_db
import psycopg2
import event_db
import logging

""""This will handle all the admin related functions"""

def check_admin(phone_number:str) -> bool | None:
    """Takes a phone number in the form of a string and returns the specific users True or False value for is_admin.
    If the number provided is not found in the users table, returns None."""
    connection, cur = None, None
    
    normalized_phone_number = event_db.normalize_phone_number(phone_number)

    if not normalized_phone_number:
        return None
    
    sql = "SELECT is_admin FROM users WHERE phone_number = %s"
    try:
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(sql, (normalized_phone_number,))

        response = cur.fetchone()

        if response:
            return response[0]
        else:
            return None
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        return None
    finally:
        event_db.close_connection(connection, cur)

def create_admin(phone_number:str):
    """Changes the is_admin value for the user provided from False to True. If no such user exists, a ValueError"""
    connection = event_db.open_connection()
    cur = connection.cursor()
    try:
        cur.execute(f"UPDATE users SET is_admin = TRUE WHERE phone_number = '{phone_number}';")
        return (f"{phone_number} now has admin priviledges.")
    except TypeError:
        return None

# def create_event():
