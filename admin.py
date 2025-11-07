import datetime
import logging

import psycopg2

import event_db
import os
import sms
from twilio.rest import Client

""""This file handles all the admin related functions"""


client = Client(
        os.environ.get('TWILIO_SID'),
        os.environ.get('TWILIO_AUTH_TOKEN')
    )
sms_sender = sms.Sms(client)


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

def add_event(code: str, date: str, name: str) -> int | None:
    """
    Admin Function: Inputs the event code, date, and name of event to create a new event in the events table of the database.
    
    Returns new event_ID if the event is successfully created or None in the event of failure.
    """

    connection, cur = None, None

    sql = "INSERT INTO events (event_code, event_name, event_date)" \
    "VALUES (%s, %s, %s) RETURNING event_id;"

    try:
        connection = event_db.open_connection()
        cur = connection.cursor()

        event_date = datetime.date.fromisoformat(date) #Converts the date str to a date object

        cur.execute(sql, (code.lower(), name, event_date))

        new_id = cur.fetchone()[0]

        connection.commit()
        return new_id
    except (psycopg2.Error, ValueError) as e:
        logging.error(f"DB Error or invalid date format in add_event: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        event_db.close_connection(connection, cur)

def delete_event(event_code:str) -> bool:
    """
    Deletes an event from the events table. If an event is deleted, the 'ON DELETE CASCADE' rule
    will cause all signups for the event to be deleted as well. Returns True if successful, False
    otherwise. 
    """
    connection, cur = None, None
    sql = "DELETE FROM events WHERE event_code = %s;"

    try: 
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(sql, (event_code.lower(),))
        rows_deleted = cur.rowcount
        connection.commit()
        return rows_deleted > 0
    except psycopg2.Error as e:
        logging.error(f"DB Error in delete_event: {e}")
        return False
    finally:
        event_db.close_connection(connection, cur)

def get_admins():
    connection, cur = None, None

    sql = "SELECT phone_number FROM users WHERE is_admin = true;"

    try:
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(sql)
        admin_list = cur.fetchall()

        admin_list = [item[0] for item in admin_list]
        return admin_list
    except Exception as e:
        logging.error(f"Error in get_admins: {e}")
        return None
    finally:
        event_db.close_connection(connection, cur)

def get_confirmation_count(event_id):
    connection, cur = None, None

    sql = "SELECT COUNT(*) FROM user_event_signups WHERE attendance_confirmed = true AND event_id = %s;"

    try:
        connection = event_db.open_connection()
        cur = connection.cursor()
        cur.execute(sql, (event_id,))
        confirmed_responses = cur.fetchone()[0]

        return confirmed_responses
    except Exception as e:
        logging.error(f"Error in get_confirmation_count: {e}")
    finally:
        event_db.close_connection(connection, cur)

def notify_event_participants(event_id, msg:str):

    phone_numbers_list = event_db.get_phone_numbers_for_event(event_id)

    for number in phone_numbers_list:
        sms_sender.send_sms(to_number=number, body=msg)
    
    return len(phone_numbers_list)
