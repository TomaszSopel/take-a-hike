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

def set_admin_status(phone_number:str, status:bool) -> bool:
    """Changes the is_admin value for the user """
    connection, cur = None, None
    
    normalized_phone_number = event_db.normalize_phone_number(phone_number)
    if not normalized_phone_number:
        return False

    query = "UPDATE users SET is_admin = %s WHERE phone_number = %s"
    
    try:
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(query, (status, normalized_phone_number))
        connection.commit()
        return cur.rowcount == 1
    except psycopg2.Error as e:
        logging.error(f"DB Error in set_admin_status: {e}")
        return False
    finally:
        event_db.close_connection(connection, cur)

def get_headcount(event_code:str) -> int | None:
    """Admin Function: Inputs an event code and outputs number of signups for that event."""
    connection, cur = None, None

    event = event_db.get_event_by_code(event_code)

    if not event:
        return None #If no event exists with the corresponding event code, return None
    
    sql = "SELECT COUNT(*) FROM user_event_signups WHERE event_id = %s;"

    try:
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(sql, (event['event_id'],))

        count = cur.fetchone()[0]
        return count
    except psycopg2.Error as e:
        logging.error(f"DB Error in get_headcount: {e}")
        return None
    finally:
        event_db.close_connection(connection, cur)
