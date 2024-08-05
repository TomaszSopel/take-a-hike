import os
import psycopg2

def connect():
    conn = psycopg2.connect(
        host = "localhost",
        port = "5432",
        database = "take_a_hike",
        password = "7890",
        user = "postgres"
    )
    return conn

connection = connect()
cur = connection.cursor()

cur.execute("SELECT version();")
result = cur.fetchone()

print(result)

cur.close()
connection.close()
