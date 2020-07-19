import sqlite3
from sqlite3 import Error
from datetime import datetime

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=10)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_user(conn, msg):
    sql = ''' INSERT OR IGNORE INTO users(email,purchased,created,lastSent,unsubscribe,deactivated)
              VALUES(?,?,?,?,?,?) 
              '''
    cur = conn.cursor()
    cur.execute(sql, msg)
    conn.commit()
    return cur.lastrowid

def insert_problem(conn, msg):
    sql = ''' INSERT OR IGNORE INTO problems(filename)
              VALUES(?)
              '''
    cur = conn.cursor()
    cur.execute(sql, msg)
    conn.commit()
    return cur.lastrowid

def update_user(conn, msg):
    sql = ''' UPDATE users
              SET email = ? ,
                  purchased = ?,
                  created = ?,
                  lastSent = ?,
                  unsubscribe = ?,
                  deactivated =? 
              WHERE id = ?'''
              
    cur = conn.cursor()
    cur.execute(sql, msg)
    conn.commit()

def update_problem(conn, msg):
    sql = ''' UPDATE problems
              SET filename = ?
              WHERE id = ?'''

    cur = conn.cursor()
    cur.execute(sql, msg)
    conn.commit()

def delete_table(conn, table):
    sql = 'DROP TABLE '+table
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def delete_all_rows(conn, table):
    sql = 'DELETE FROM '+table
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def delete(conn, table, id):
    sql = 'DELETE FROM '+table+' WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()
    return rows

if __name__ == '__main__':
    DATABASE_NAME = r"./sqlite.db"

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    email text,
                                    purchased boolean NOT NULL,
                                    created datetime,
                                    lastSent datetime,
                                    unsubscribe boolean NOT NULL,
                                    deactivated boolean NOT NULL,
                                    UNIQUE(email)
                                    )
                                    ;"""

    sql_create_problems_table = """CREATE TABLE IF NOT EXISTS problems (
                                    pid integer PRIMARY KEY,
                                    filename text,
                                    UNIQUE(filename)
                                );"""

    conn = create_connection(DATABASE_NAME)
    try:
        delete_table(conn, 'users')
        delete_table(conn, 'problems')
    except:
        pass

    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_problems_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        prob1 = ['./compendium/findx.pdf']
        prob2 = ['./compendium/findy.pdf']

        insert_problem(conn, prob1)
        insert_problem(conn, prob2)

        user1 = ['reinaldomaslim@gmail.com', 0, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), 0, 0]
        user2 = ['e0403962@u.nus.edu', 0, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), 0, 0]
        
        insert_user(conn, user1)
        insert_user(conn, user2)

        users = select_all(conn, 'users')   
        print(users)

        # delete(conn, 'users', 1)