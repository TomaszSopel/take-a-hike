import os
import psycopg2
import logging
import re

def open_connection():
    return psycopg2.connect(
        host = os.environ.get('HOST'),
        port = os.environ.get('DB_PORT'),
        database = os.environ.get('DATABASE'),
        password = "" if os.environ.get('PASSWORD') is None else os.environ.get('PASSWORD'),
        user = os.environ.get('USER'),
    )

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

#TODO 1: write code that says, "if no password treat it as an empty string"

def get_user(number:str):
    """Inputs a single phone number (str) and returns a single user_id (int)
    if they are in the users table, otherwise returns None"""
    number = normalize_phone_number(number)

    sql = "SELECT user_id FROM users WHERE phone_number = %s;"
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(sql, (number,))
        user_id = cur.fetchone()
        if user_id:
            print(f"user_id is {user_id[0]}")
            return user_id[0]
        else:
            print("get_user failed: User not found in users table.")
            return None
    except psycopg2.Error as e:
        logging.error(f"DB Error in get_user: {e}")
        return None
    finally:
        close_connection(connection, cur)

def get_phone(id:int):
    """Inputs a user id (int) and returns their corresponding phone number (str). If not found, returns 0."""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT phone_number FROM users WHERE user_id = '{id}'")
        id = cur.fetchone()
        return id[0]
    except TypeError:
        return 0
    finally:
        close_connection(connection, cur)

def log_user(number:str):
    """Inputs a phone number, if it already doesn't exist in the users table,
    it will add it. """
    if get_user(number) is None:
        try:
            number = normalize_phone_number(number)
            connection = open_connection()
            cur = connection.cursor()
            cur.execute(f"INSERT INTO users (phone_number) VALUES ({number});")
            connection.commit()
            print(f"New user added, phone number: {number}")
        finally:
            close_connection(connection, cur)
    else:
        print("User already exists in users table.")
        return None

def get_event_id(code:str):
    """Inputs an event event code (str) and checks if the corresponding event 
    exists in the events table, returning event id (int), otherwise False"""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT event_id FROM events WHERE event_code = '{code.lower()}'")
        event_id = cur.fetchone()
        return event_id[0]
    except TypeError:
        return False
    finally:
        close_connection(connection, cur)

# TODO 1: Modify sign_up() to refuse duplicate signups
def sign_up(user_id:int, event_id:int):
    """Inputs user id and event id and logs them into the user_events_signup table."""
    try:
        connection = open_connection()
        cur = connection.cursor()
        print(f"Function: Sign_up(), user_id is {user_id} and event_id is {event_id}")
        check = cur.execute(f"SELECT * FROM user_event_signups WHERE user_id = {user_id} AND event_id = {event_id};")
        check = cur.fetchone()
        print(f"sign_up() --> check is {check}")
        if check is not None: #If a check exists, then it's already been entered on the user_event_signups table
            print("Entry already exists. Returning None")
            return None
        else:
            cur.execute(f"INSERT INTO user_event_signups (user_id, event_id) VALUES ({user_id},{event_id});")
            connection.commit()
            print("entry logged")
            return True
    except psycopg2.errors.ForeignKeyViolation:
        print("File not Found: You can control this error!!!")
    finally:
        close_connection(connection, cur)

def event_get_numbers(event_id:int):
    """Inputs an event code (int) and returns all phone numbers signed up for the event (list[int])"""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT user_id FROM user_event_signups WHERE event_id = {event_id};")
        return (cur.fetchall())
    except:
        print("Error")
    finally:
        close_connection(connection, cur)

def get_events():
    """Returns all events currently registered"""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT event_code FROM events;")
        raw_events_list = cur.fetchall()
        events_list = [str(item).replace(",", "").replace("(", "").replace(")", "").replace("'", "") for item in raw_events_list] #Converts output into a list of strings
        return (events_list)
    except:
        print("Error")
    finally:
        close_connection(connection, cur)

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
    
    connection = None
    cursor = None

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
    connection = None
    cur = None

    sql = "DELETE FROM user_event_signups WHERE user_id = %s AND event_id = %s;"
    
    try:
        connection = open_connection()
        cur = connection.cursor()

        cur.execute(sql, (user_id, event_id))

        rows_deleted = cur.rowcount

        connection.commit()

        # Return True if a row was deleted, False otherwise.
        return rows_deleted > 0

    except psycopg2.Error as e:
        logging.error(f"Database error in cancel_signup: {e}")
        return False
    finally:
        close_connection(connection, cur)

"""
def add_event(event_name, date, location, code, description)
    This will implement the addition of an event to the events table via SMS, 
    likely through a multi-SMS chain implemented via the sms_database bridge, 
    which data will then get fed into this function.
"""