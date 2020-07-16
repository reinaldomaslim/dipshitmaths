import sqlite3
from sqlite3 import Error
from datetime import datetime
from create import *

#everyday at specific time: morning send question, night send answer 
#loop thru mail database
#send email with the right problem
#via ses api

if __name__ == '__main__':
    DATABASE_NAME = r"./sqlite.db"
    conn = create_connection(DATABASE_NAME)
