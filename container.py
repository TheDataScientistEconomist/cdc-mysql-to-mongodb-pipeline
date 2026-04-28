import os, sys, subprocess, time, yaml
import mysql.connector as connector

# -------------------
# RUN SHELL COMMAND
# -------------------

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result.returncode

# ----------------------
# DELETE CONTAINERS
# ----------------------

def delete(container):
    run_cmd(f"docker rm -f {container}")
    print(f"Removed {container}.")

def delete_all():
    delete("some-mysql")
    delete("some-mongo")

# ------------------
# CREATE CONTAINER
# ------------------
def create(db):
    if db == "mysql":
        password = os.environ.get("MYSQL_ROOT_PASSWORD")

        if not password:
            print("Error: MYSQL_ROOT_PASSWORD not set")
            return

        cmd = (
            f"docker run -p 3307:3306 "
            f"--name some-mysql "
            f"-e MYSQL_ROOT_PASSWORD={password} "
            f"-d mysql"
        )
    elif db == "mongodb":
        cmd = "docker run -p 27017:27017 --name some-mongo -d mongo"
    else:
        print(f"Unknown database: {db}")

    result_code = run_cmd(cmd)

    if result_code == 0:
        print(f"{db} container created successfully.")
    else:
        print(f"Failed to create {db} container.")

def create_all():
    create("mysql")
    create("mongodb")


# ----------------------
# INITIALIZE MYSQL DB
# ----------------------

def init_mysql():
    with open("db.yaml", "r") as f:
        db = yaml.safe_load(f)

    cnx = connector.connect(
        port=db["port"],
        user=db["user"],
        password=db["password"],
        host=db["host"],
        auth_plugin="mysql_native_password"
    ) 
    # create cursor
    cursor = cnx.cursor()

    # delete previous db, create and use new one
    cursor.execute("DROP DATABASE IF EXISTS pluto")
    cursor.execute("CREATE DATABASE IF NOT EXISTS pluto")
    cursor.execute("USE pluto")

    # create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id VARCHAR(36),
            stamp VARCHAR(20)
        )
    """)

    # clean up
    cnx.commit()
    cursor.close()
    cnx.close()

    print("Database pluto and table posts created successfully.")

# read input argument within the main router
if __name__ == "__main__":
    argument = sys.argv[1] if len(sys.argv) > 1 else None

    if argument == "-create":
        create_all()

    elif argument == "-init":
        init_mysql()

    elif argument == "-delete":
        delete_all()

    else:
        print("Usage:")
        print("  python containers.py -create")
        print("  python containers.py -init")
        print("  python containers.py -delete")





