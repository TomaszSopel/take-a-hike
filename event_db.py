import os
import psycopg2

def connect():
    conn = psycopg2.connect(
        host = os.getenv('POSTGRES_HOST'),
        database = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD')
    )
    return conn

connection = connect()
cur = connection.cursor()

cur.execute("SELECT version();")
result = cur.fetchone()

print(result)

cur.close()
connection.close()
