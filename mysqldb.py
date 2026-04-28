import os, sys, subprocess, uuid, yaml
from datetime import datetime
import mysql.connector as connector


# establish database connection
def get_connection(database=None):
    with open("db.yaml", "r") as f:
        db = yaml.safe_load(f)

    config = {
        "host": db["host"],
        "port": db["port"],
        "user": db["user"],
        "password": db["password"],
        "auth_plugin": "mysql_native_password"
    }

    if database:
        config["database"] = database

    return connector.connect(**config)

# initialize connection and create database after deleting any existing one
def init_mysql():
    cnx = get_connection()
    cursor = cnx.cursor()

    cursor.execute("DROP DATABASE IF EXISTS `pluto`")
    cursor.execute("CREATE DATABASE IF NOT EXISTS `pluto`")
    cursor.execute("USE pluto")

    # create posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id VARCHAR(36),
            stamp VARCHAR(30)
        )
    """)

    cnx.commit()
    cursor.close()
    cnx.close()

    print("Database pluto and table posts created successfully.")

# write stamps to posts table
def write():
    cnx = get_connection("pluto")
    cursor = cnx.cursor()

    post_id = str(uuid.uuid4())
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = "INSERT INTO posts (id, stamp) VALUES (%s, %s)"
    cursor.execute(query, (post_id, stamp))

    cnx.commit()
    cursor.close()
    cnx.close()

    print(f"Inserted MySQL record: {stamp}")

# read posts table
def read():
    cnx = get_connection("pluto")
    cursor = cnx.cursor()

    query = """
        SELECT stamp
        FROM posts
        ORDER BY stamp DESC
        LIMIT 5
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()

    return [row[0] for row in rows]

# delete posts table data
def delete():
    cnx = get_connection("pluto")
    cursor = cnx.cursor()

    cursor.execute("TRUNCATE posts")

    cnx.commit()
    cursor.close()
    cnx.close()

    print("Deleted MySQL posts data.")

if __name__ == "__main__":
    argument = sys.argv[1] if len(sys.argv) > 1 else None

    if argument == "-init":
        init_mysql()

    else:
        print("Usage:")
        print("  python mysqldb.py -init")