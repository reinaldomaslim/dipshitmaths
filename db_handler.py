from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, DateTime, MetaData
from sqlalchemy.sql import select
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
    Column("deactivated", Boolean, nullable=False)
)

Problems = Table(
    "problems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String(length=200), unique=True, nullable=False)
)


class DBHandler:

    def __init__(self, db_path):
        self._db_path = db_path
        self._engine = create_engine(f"sqlite:///{self._db_path}", echo=False)
        self._conn = self._engine.connect()
        self._users = Users
        self._problems = Problems
        metadata.create_all(self._engine)

        self._initialize_db()

    def _initialize_db(self):
        # Dummy users
        self.insert_user(
            email="reinaldomaslim@gmail.com",
            purchased=False,
            lastSent=datetime.now(),
            unsubscribed=False,
            deactivated=False
        )
        self.insert_user(
            email="e0403962@u.nus.edu",
            purchased=False,
            lastSent=datetime.now(),
            unsubscribed=False,
            deactivated=False
        )

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
            deactivated=deactivated
        )
        self._conn.execute(ins)

    def insert_problem(self, filename):
        ins = self._problems.insert().prefix_with("OR IGNORE").values(
            filename=filename
        )
        self._conn.execute(ins)

    def _users_select_all(self):
        return select([self._users])
