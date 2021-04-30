import sqlite3
from src.constants import CommonConstants


class DbConnection:
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(CommonConstants.DB_PATH)

    def get_connection(self):
        return self.conn
