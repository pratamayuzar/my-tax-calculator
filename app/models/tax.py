import pymysql
from lib.general import General
from lib.db import Db


class TaxModel(General):

    TABLE = "tax"

    def __init__(self):
        General.__init__(self)
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.db = Db(self.conn, self.cursor)

    def select(self):
        try:
            self.db.select(self.TABLE)
            return self.db.execute()
        except Exception:
            raise

    def insert(self, data):
        try:
            self.db.insert(self.TABLE, data)
            return self.db.execute()
        except Exception:
            raise
