from threading import Timer
import time, sys, mysqldb, mongodb


timer = None

# delete data in all dbs
def clearout():
    mysqldb.delete()
    mongodb.delete()
    print("Deleted data in all dbs!")

# time loop
def status(stamps, db):
    print(f"Data in {db}:")
    for stamp in stamps:
        print(stamp)
    time.sleep(2)

def write_mysql():
    mysqldb.write()

def sync_mysql_to_mongo():
    stamps = mysqldb.read()
    status(stamps, "mysql")
    mongodb.write(stamps)

def verify_mongo():
    stamps = mongodb.read()
    status(stamps, "mongo")

def timeloop():
    global timer

    try:
        print(f"--- LOOP: {time.ctime()} ---")
        write_mysql()
        sync_mysql_to_mongo()
        verify_mongo()

    except Exception as e:
        print(f"Error during loop: {e}")

    timer = Timer(5, timeloop)
    timer.start()

def stop_timer():
    global timer

    if timer:
        timer.cancel()
        print("Timer Cancelled")


if __name__ == "__main__":
    argument = sys.argv[1] if len(sys.argv) > 1 else None

    if argument == "-clear":
        clearout()
        sys.exit()

    timeloop()