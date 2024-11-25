import os
import psycopg2

def open_connection():
    db_url = os.environ.get('DB_URL')
    
    if not db_url:
        raise ValueError("No DB_URL found in environment variables.")
    
    return psycopg2.connect(
        # host = os.environ.get('HOST'),
        # port = os.environ.get('DB_PORT'),
        # database = os.environ.get('DATABASE'),
        # password = "" if os.environ.get('PASSWORD') is None else os.environ.get('PASSWORD'),
        # user = os.environ.get('USER')
        db_url,
        sslmode='require'
    )

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection:
        cursor.connection.close()

#TODO 1: write code that says, "if no password treat it as an empty string"

def get_user(number:str):
    """Inputs a single phone number (str) and returns a single user_id (int)
    if they are in the users table, otherwise returns FALSE"""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE phone_number = '{number}'")
        user_id = cur.fetchone()
        return user_id[0]
    except TypeError:
        return False
    finally:
        close_connection(connection, cur)

def get_phone(id:int):
    """Inputs a user id (int) and returns their corresponding phone number (str). If not found, returns False."""
    try:
        connection = open_connection()
        cur = connection.cursor()
        cur.execute(f"SELECT phone_number FROM users WHERE user_id = '{id}'")
        id = cur.fetchone()
        return id[0]
    except TypeError:
        return False
    finally:
        close_connection(connection, cur)

def log_user(number:str):
    """Inputs a phone number, if it already doesn't exist in the users table,
    it will add it."""
    if get_user(number) is False:
        try:
            connection = open_connection()
            cur = connection.cursor()
            cur.execute(f"INSERT INTO users (phone_number) VALUES ({number});")
            connection.commit()
            print(f"New user added, phone number: {number}")
        finally:
            close_connection(connection, cur)
    else:
        pass

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
        cur.execute(f"INSERT INTO user_event_signups (user_id, event_id) VALUES ({user_id},{event_id});")
        connection.commit()
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
        return (cur.fetchall())
    except:
        print("Error")
    finally:
        close_connection(connection, cur)
