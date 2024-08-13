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
    """Inputs a single phone number (str) and returns a single user_id (int)"""
    cur.execute(f"SELECT user_id FROM users WHERE phone_number = '{number}'")
    user_id = cur.fetchone()
    return user_id[0]

print(get_user("1234567890"))

def get_number(id:int):
    """Inputs a user id (int) and returns their corresponding phone number (str)"""
    cur.execute(f"SELECT phone_number FROM users WHERE user_id = '{id}'")
    id = cur.fetchone()
    return id[0]

print(get_number(1))

# cur.close()
# connection.close()
