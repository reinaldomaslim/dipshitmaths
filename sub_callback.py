import sqlite3
from sqlite3 import Error
from datetime import datetime

#wait for new subscriber
#append to database
#send welcome msg

#wait for new pro sub
#change status in db
#send thanks msg

#wait for unsub or deactivation
#remove from database

if __name__ == '__main__':
    DATABASE_NAME = r"./sqlite.db"

    conn = create_connection(DATABASE_NAME)

