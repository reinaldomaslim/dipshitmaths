from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, DateTime, MetaData
from sqlalchemy.sql import select, delete
from datetime import datetime

metadata = MetaData()

# Tables
# TODO: Discuss column attributes' constraints
Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(length=100), nullable=False, unique=True),
    Column("purchased", Boolean, nullable=False),
    Column("created", DateTime),
    Column("lastSent", DateTime),
    Column("unsubscribed", Boolean, nullable=False),
    Column("deactivated", Boolean, nullable=False))

Problems = Table(
    "problems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String(length=200), unique=True, nullable=False))

EmailConfirmation = Table(
    "email-confirmation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(length=100), nullable=False, unique=True),
    Column("created", DateTime, nullable=False),
    Column("referid", String(length=100), nullable=False))


class DBEngine:
    def __init__(self, db_path):
        self._db_path = db_path
        self._engine = create_engine(f"sqlite:///{self._db_path}", echo=True)
        self._conn = self._engine.connect()
        self._users = Users
        self._problems = Problems
        self._email_confirmation = EmailConfirmation
        metadata.create_all(self._engine)
        self._initialize_db()

    @property
    def handler(self):
        return self

    def _initialize_db(self):
        # Dummy users
        self.insert_user(
            email="reinaldomaslim@gmail.com",
            purchased=False,
            lastSent=datetime.now(),
            unsubscribed=False,
            deactivated=False)
        self.insert_user(
            email="e0403962@u.nus.edu",
            purchased=False,
            lastSent=datetime.now(),
            unsubscribed=False,
            deactivated=False)

        # Dummy problems
        self.insert_problem("./compendium/findx.pdf")
        self.insert_problem("./compendium/findy.pdf")
        print(self._users_select_all())

    def insert_user(self, email, purchased, lastSent, unsubscribed, deactivated):
        ins = self._users.insert().prefix_with("OR IGNORE").values(
            email=email,
            purchased=purchased,
            created=datetime.now(),
            lastSent=lastSent,
            unsubscribed=unsubscribed,
            deactivated=deactivated)
        self._conn.execute(ins)

    def insert_email_confirmation(self, email, referid):
        ins = self._email_confirmation.insert().prefix_with("OR IGNORE").values(
            email=email,
            created=datetime.now(),
            referid=referid)
        self._conn.execute(ins)

    def select_email_confirmation(self, email):
        ins = select([self._email_confirmation]).where(self._email_confirmation.c.email == email)
        result = self._conn.execute(ins).fetchone()
        return dict(result or {})

    def delete_email_confirmation(self, email):
        ins = self._email_confirmation.delete().where(self._email_confirmation.c.email == email)
        self._conn.execute(ins)

    def insert_problem(self, filename):
        ins = self._problems.insert().prefix_with("OR IGNORE").values(filename=filename)
        self._conn.execute(ins)

    def _users_select_all(self):
        ins = select([self._users])
        result = self._conn.execute(ins)
        return [dict(row) for row in result]
