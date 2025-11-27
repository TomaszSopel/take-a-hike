import datetime
import logging
import os
import re

import psycopg


def open_connection() -> psycopg.Connection:
    return psycopg.connect(
        host = os.environ.get('HOST'),
        port = os.environ.get('DB_PORT'),
        dbname = os.environ.get('DATABASE'),
        password = "" if os.environ.get('PASSWORD') is None else os.environ.get('PASSWORD'),
        user = os.environ.get('USER'),
    )

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

def get_connection_string():
    """
    Constructs the connection string to be reused for passing into functions.
    Prioritizes the 'DATABASE_URL' environment variable on Heroku,
    Falls back to local environment variables for local testing.
    """
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        return db_url
    else:
        return (
            f"host={os.environ.get('HOST')} "
            f"port={os.environ.get('DB_PORT')} "
            f"dbname={os.environ.get('DATABASE')} "
            f"user={os.environ.get('USER')} "
            f"password={os.environ.get('PASSWORD')}"
        )

def get_user(number:str):
    """Inputs a single phone number (str) and returns a single user_id (int)
    if they are in the users table, otherwise returns None"""
    normalized_number = normalize_phone_number(number)
    if not normalized_number:
        return None

    sql = "SELECT user_id FROM users WHERE phone_number = %s;"
    
    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute(sql, (normalized_number,))
            row = response.fetchone()
            if row:
                user_id = row[0]
                return user_id
            else:
                print("get_user failed: User not found in users table.")
                return None

    except psycopg.Error as e:
        logging.error(f"DB Error in get_user: {e}")
        return None

def get_phone(user_id:int):
    """Inputs a user id (int) and returns their corresponding phone number (str). If not found, returns None."""

    sql = "SELECT phone_number FROM users WHERE user_id = %s"
    
    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute(sql, (user_id,)) # Pass user_id as a tuple
            row = response.fetchone()
        
            if row:
                return row[0]
            else:
                return None # Return None if not found
            
    except psycopg.Error as e:
        logging.error(f"Error in get_phone: {e}")
        return None

def log_user(phone_number: str):
    """Takes a phone number (str) and logs it into the users table."""

    normalized_number = normalize_phone_number(phone_number)
    if not normalized_number:
        return
    
    sql = "INSERT INTO users (phone_number) VALUES (%s) ON CONFLICT (phone_number) DO NOTHING;"
    try:
        with psycopg.connect(get_connection_string()) as connection:
            connection.execute(sql, (normalized_number,))
            connection.commit()
    except psycopg.Error as e:
        logging.error(f"DB Error in log_user: {e}")
    
def get_event_id(code:str):
    """Inputs an event event code (str) and checks if the corresponding event 
    exists in the events table, returning event id (int), otherwise None"""

    sql = "SELECT event_id FROM events WHERE event_code = %s"
    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute(sql, (code.lower(),))
            row = response.fetchone()
    
            if row == None:
                return None
            else:
                return row[0]
    except psycopg.Error as e:
        logging.error(f"DB Error in get_event_id: {e}")


# TODO 1: Modify sign_up() to refuse duplicate signups
def sign_up(user_id:int, event_id:int):
    """Inputs user id and event id and logs them into the user_events_signup table."""

    sql = "SELECT * FROM user_event_signups WHERE user_id = %s AND event_id = %s;"

    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute(sql, (user_id, event_id))
            check = response.fetchone()

            if check is not None: #If a check exists, then it's already been entered on the user_event_signups table
                print("Entry already exists. Returning None")
                return None
            else:
                sql = "INSERT INTO user_event_signups (user_id, event_id) VALUES (%s, %s);"
                connection.execute(sql, (user_id,event_id))
                connection.commit()
                print("entry logged")
                return True
    except psycopg.errors.ForeignKeyViolation:
        logging.error(f"Signup Failed: UserID {user_id} or EventID {event_id} does not exist.")
        return False
    
    except psycopg.Error as e:
        logging.error(f"Error in sign_up: {e}")
        return None


def get_user_ids_for_event(event_id:int):
    """Inputs an event code (int) and returns all user ID's signed up for the event (list[int]). """

    sql = "SELECT user_id FROM user_event_signups WHERE event_id = %s;"

    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute(sql, (event_id,))
            rows = response.fetchall()
            user_id_list = [row[0] for row in rows]
            return user_id_list
    except psycopg.Error as e:
        logging.error(f"Error in get_user_ids_for_event: {e}")
        return [] # Returns an empty list instead of failing. 
        
def get_events():
    """Returns all events currently registered"""

    try:
        with psycopg.connect(get_connection_string()) as connection:
            response = connection.execute("SELECT event_code FROM events;")
            rows = response.fetchall()
            events_list = [item[0] for item in rows]
            return events_list
    except psycopg.Error as e:
        logging.error(f"Error in get_events: {e}")
        return []
    
def normalize_phone_number(phone_number:str) -> str | None:
    """Takes a phone number in the form of a string and normalizes it to a E.164 format."""
    if not phone_number:
        return None
    
    phone_number = re.sub(r'\D', '', phone_number)  # Remove all non-digit characters from phone_number
    
    if len(phone_number) == 10:  # If the phone number is 10 digits long, assume it's a US number
        normalized_number = f"1{phone_number}"  # Add country code for US

    elif len(phone_number) == 11 and phone_number.startswith('1'): 
        # If the phone number is 11 digits long and starts with '1', assume it's a US number
        normalized_number = phone_number # Already in E.164 format
    else:
        return None
    
    return f"+{normalized_number}"  # Ensure it starts with a '+' for E.164 format


def get_event_by_code(event_code:str) -> dict | None:
    """Takes the event code for a particular event, and returns the event_id, event_name, event_date, event_description, and event_location
    that corresponds with the event_code; returned as a dictionary."""   
    connection, cur = None, None
    sql = """
        SELECT event_id, event_name, event_code, event_date, event_description, event_location
        FROM events
        WHERE event_code = %s;
    """
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(sql, (event_code.lower(),))
        event_info = cur.fetchone()
        
        if event_info:
            event_dict = {
                'event_id': event_info[0],
                'event_name': event_info[1],
                'event_code': event_info[2],
                'event_date': event_info[3],
                'event_description': event_info[4],
                'event_location': event_info[5]
            }
            return event_dict
        else:
            return None

    except Exception as e:
        logging.error(f"Error in get_event_by_code: {e}")
        return None
    finally:
        close_connection(connection, cur)

def cancel_signup(user_id:int, event_id:int):
    """Cancels a user's signup for an event by removing the entry from the user_event_signups table.
    Returns True if the cancellation was successful, False otherwise."""
    connection, cur = None, None
    sql = "DELETE FROM user_event_signups WHERE user_id = %s AND event_id = %s;"
    
    try:
        connection = open_connection()
        cur = connection.cursor()

        cur.execute(sql, (user_id, event_id))

        rows_deleted = cur.rowcount

        connection.commit()

        # Return True if a row was deleted, False otherwise.
        return rows_deleted > 0

    except psycopg.Error as e:
        logging.error(f"Database error in cancel_signup: {e}")
        return False
    finally:
        close_connection(connection, cur)

def get_events_for_date(target_date: datetime.date = None) -> list:
    """Retrieves all events that are scheduled to happen at a certain date.
    If no date is provided, then defaults to tommorows date.
    Returns empty list if no events are scheduled for target date"""
    
    connection, cur = None, None
    
    if target_date is None:
        target_date = datetime.date.today() + datetime.timedelta(days=1)

    sql = "SELECT event_id, event_name, event_code FROM events WHERE event_date = %s;"
    
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(sql, (target_date,))
        events = []
        for row in cur.fetchall():
            events.append({
                'event_id': row[0],
                'event_name': row[1],
                'event_code': row[2]
            })
        return events
    except psycopg.Error as e:
        logging.error(f"DB Error in get_events_for_date: {e}")
        return []
    
    finally:
        close_connection(connection, cur)

def confirm_attendance(user_id:int, event_id:int) -> bool:
    """"
    Changes the attendance_confirmed value for a user-event-signup from False to True.
    Returns True if update was successful (1 row changed), otherwise False.
    """
    connection, cur = None, None
    sql = "UPDATE user_event_signups SET attendance_confirmed = true WHERE user_id = %s and event_id = %s;"
    
    try:
        connection = open_connection()
        cur = connection.cursor()

        cur.execute(sql, (user_id, event_id))

        connection.commit()

        #If a value was updated, it will return True, False otherwise
        return cur.rowcount == 1

    except psycopg.Error as e:
        logging.error(f"Database error in confirming attendance: {e}")
        return False
    finally:
        close_connection(connection, cur)

def get_phone_numbers_for_event(event_id):
    connection, cur = None, None

    sql = "" \
    "SELECT phone_number from users " \
    "JOIN user_event_signups " \
    "ON users.user_id=user_event_signups.user_id " \
    "WHERE user_event_signups.event_id=%s;"

    try:
        connection = open_connection()
        cur = connection.cursor()

        cur.execute(sql, (event_id,))
        phone_number_list = cur.fetchall()

        phone_number_list = [item[0] for item in phone_number_list]

        return phone_number_list
    except psycopg.Error as e:
        logging.error(f"Database error in getting phone numbers for event: {e}")
        return []
    finally:
        close_connection(connection, cur)


"""
def add_event(event_name, date, location, code, description)
    This will implement the addition of an event to the events table via SMS, 
    likely through a multi-SMS chain implemented via the sms_database bridge, 
    which data will then get fed into this function.
"""