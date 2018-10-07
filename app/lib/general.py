import pymysql
from DBUtils.PersistentDB import PersistentDB


class General:
    def __init__(self):
        self.pool = PersistentDB(
            pymysql,
            host='localhost',
            user='root',
            passwd='',
            db='tax_calculator',
            charset='utf8',
            autocommit=True
        )
