import os
import psycopg2

HOST = 'localhost'
PORT = '5432'
DATABASE = "take_a_hike"
USER = "gitpod"



def connect():
    conn = psycopg2.connect(
        host = HOST,
        port = PORT,
        database = DATABASE,
        # password = "7890",
        user = USER
    )
    return conn

connection = connect()
cur = connection.cursor()

# cur.execute("SELECT * FROM users;")
# result = cur.fetchone()
# print(result)

def get_user(number:str):
    """Inputs a single phone number (str) and returns a single user_id (int)
    if they are in the users table, otherwise returns FALSE"""
    try:
        cur.execute(f"SELECT user_id FROM users WHERE phone_number = '{number}'")
        user_id = cur.fetchone()
        return user_id[0]
    except TypeError:
        return False

def get_number(id:int):
    """Inputs a user id (int) and returns their corresponding phone number (str)"""
    cur.execute(f"SELECT phone_number FROM users WHERE user_id = '{id}'")
    id = cur.fetchone()
    return id[0]

def log_number(number:str):
    """Inputs a phone number, if it already doesn't exist in the events table,
    it will add it."""
    if get_user(number) is False:
        cur.execute(f"INSERT INTO users (phone_number) VALUES ({number});")
        print(f"New user added, phone number: {number}")
    else:
        pass

log_number('2345678901')
# cur.close()
# connection.close()
