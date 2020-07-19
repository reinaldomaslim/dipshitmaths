import sqlite3
from sqlite3 import Error
from datetime import datetime


class DBHandler:

    def __init__(self, db_file):
        # Create DB
        try:
            self.conn = sqlite3.connect(db_file, timeout=10)
        except Error as e:
            print(e)
            exit(0)
        except Exception as e:
            print(e)
            exit(0)

        # Flush tables
        self.delete_table("users")
        self.delete_table("problems")

        # Initialize tables and problems
        self._initialize_tables()
        self._add_dummy_problems()

    def create_table(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
        except Error as e:
            print(e)

    def insert_problem(self, msg):
        sql = ''' INSERT OR IGNORE INTO problems(filename)
                  VALUES(?)
              '''
        cur = self.conn.cursor()
        cur.execute(sql, msg)
        self.conn.commit()
        return cur.lastrowid

    def insert_user(self, msg):
        sql = ''' INSERT OR IGNORE INTO users(email,purchased,created,lastSent,unsubscribe,deactivated)
                  VALUES(?,?,?,?,?,?) 
              '''
        cur = self.conn.cursor()
        cur.execute(sql, msg)
        self.conn.commit()
        return cur.lastrowid

    def select_all(self, table):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM " + table)
        rows = cur.fetchall()
        return rows

    def update_problem(self, msg):
        sql = ''' UPDATE problems
                SET filename = ?
                WHERE id = ?'''

        cur = self.conn.cursor()
        cur.execute(sql, msg)
        self.conn.commit()

    def update_user(self, msg):
        sql = ''' UPDATE users
                SET email = ? ,
                    purchased = ?,
                    created = ?,
                    lastSent = ?,
                    unsubscribe = ?,
                    deactivated =? 
                WHERE id = ?'''

        cur = self.conn.cursor()
        cur.execute(sql, msg)
        self.conn.commit()

    def delete_table(self, table):
        try:
            sql = 'DROP TABLE '+table
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        except Error as e:
            print(e)
        except Exception as e:
            print(e)

    def delete_all_rows(self, table):
        sql = 'DELETE FROM ' + table
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def delete(self, table, id):
        sql = 'DELETE FROM ' + table + ' WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def _add_dummy_problems(self):
        with self.conn:
            # Add dummy problems
            prob1 = ['./compendium/findx.pdf']
            prob2 = ['./compendium/findy.pdf']
            self.insert_problem(prob1)
            self.insert_problem(prob2)

            # Add dummy users
            user1 = ['reinaldomaslim@gmail.com', 0, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), 0, 0]
            user2 = ['e0403962@u.nus.edu', 0, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), 0, 0]
            self.insert_user(user1)
            self.insert_user(user2)

            print(self.select_all("users"))

    def _initialize_tables(self):
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
        self.create_table(sql_create_users_table)

        sql_create_problems_table = """CREATE TABLE IF NOT EXISTS problems (
                                    pid integer PRIMARY KEY,
                                    filename text,
                                    UNIQUE(filename)
                                    );"""
        self.create_table(sql_create_problems_table)
