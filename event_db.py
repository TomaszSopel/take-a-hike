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

cur.execute("SELECT * FROM users;")
result = cur.fetchall()
print(result)

# def get_user(number:str):
#     id = cur.execute("SELECT user_id FROM users WHERE phone_number = f'{number}'")
#     print(id)

# get_user('8609673158')

cur.close()
connection.close()
