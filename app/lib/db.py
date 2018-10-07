import pymysql

__author__ = 'yuzar'


def x_str(s):
    return '' if s is None else str(s)


class Db:

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.status = None
        self.q_where = None
        self.q_join = None
        self.q_update_set = None
        self.q_order = None
        self.q_group_by = None
        self.q_limit = None
        self.sql = None
        self.sql_count = None

    def reset_var(self, key=None):
        """
        Reset main variable
        :param key: string key of variable global
        :return: Set variable global to None
        """
        dic = vars(self)
        if not key:
            var_exceptions = ['conn', 'cursor']
            for i in dic.keys():
                if i not in var_exceptions:
                    dic[i] = None
        else:
            dic[key] = None

    def select(self, table, alias='', field="*"):
        """
        Select Function
        :param table: string
        :param alias: string
        :param field: string
        :return: Set main sql query
        """
        if isinstance(field, list):
            field = ", ".join(field)

        self.status = 'SELECT'
        self.sql = "SELECT {} FROM {}".format(field, table, alias)
        self.sql_count = "SELECT count(*) AS rowscount FROM {}".format(table)

    def join(self, table, alias='', using=None, on=None, join_type=''):
        """
        Join function
        :param table: string
        :param alias: string
        :param using: string
        :param on: string
        :param join_type: string -> LEFT|RIGHT|INNER
        :return: Set main query join
        """

        condition = ''
        if using:
            condition = "USING({})".format(using)
        elif on:
            condition = "ON {}".format(on)
        if join_type.upper() not in ['LEFT', 'RIGHT', 'INNER']:
            join_type = ''
        q_join = "{} JOIN {} {} {}".format(join_type.upper(), table, alias, condition)

        if self.q_join:
            self.q_join = "{} {}".format(self.q_join, q_join)
        else:
            self.q_join = q_join

    def where(self, condition, operator='AND'):
        """
        Where Function
        :param condition: string
        :param operator: string -> AND|OR
        :return: Set main query where
        """
        if self.q_where:
            self.q_where = "{} {} {}".format(self.q_where, operator, condition)
        else:
            self.q_where = '{}'.format(condition)

    def exact_where(self, column, value, operator='AND'):
        """
        Exact where Function
        :param column: string
        :param value: string
        :param operator: string -> AND|OR
        :return: Call Where function with check value condition
        """
        if value is not None or value == 0:
            value = str(value)
        if column and value:
            if value == 'null':
                condition = "{} IS NULL".format(column)
            else:
                condition = "{} = '{}'".format(column, pymysql.escape_string(str(value)))
            self.where(condition, operator)

    def query(self, sql):
        """
        Query Function
        :param sql: string -> mysql query
        :return: Set sql main query
        """
        self.status = 'QUERY'
        self.sql = sql

    def delete(self, table):
        """
        Delete Function
        :param table: string
        :return: Set delete sql main query
        """
        self.status = "DELETE"
        self.sql = "DELETE FROM {}".format(table)

    def update(self, table, data=None):
        """
        Update Function
        :param table: string
        :param data: dictionary
        :return: Set update sql main query
        """
        self.status = "UPDATE"
        if data:
            for column, value in data.items():
                self.update_set(column, value)

        set_clause = ", ".join(self.q_update_set)
        self.sql = "UPDATE {} SET {}".format(table, set_clause)

    def update_set(self, column, value, inc=None):
        """
        Update set Function
        :param column: string
        :param value: string
        :param inc: boolean -> True|False
        :return: Set update query main
        """
        if not self.q_update_set:
            self.q_update_set = list()

        if column and value:  # while value is null
            if isinstance(value, str):
                value = pymysql.escape_string(value)

            if inc is None:
                if value == 'null':
                    self.q_update_set.append("{} = NULL".format(column))
                else:
                    self.q_update_set.append("{} = '{}'".format(column, value))
            elif inc is False:
                self.q_update_set.append("{0} = {0} - {1}".format(column, value))
            else:
                self.q_update_set.append("{0} = {0} + {1}".format(column, value))

    def insert(self, table, data, is_ignore=False, is_update_field_id=False):
        """
        Insert Function
        :param table: string
        :param data: dictionary
        :param is_ignore: boolean -> True|False
        :param is_update_field_id: boolean -> True|False
        :return: Set insert sql query main
        """
        self.status = "INSERT"
        update_field = []
        if not isinstance(data, dict):
            raise Exception('Data must be dictionary')

        fields = []
        values = []
        for d in data:
            fields.append(d)
            values.append('NULL' if data[d] is None else pymysql.escape_string(str(data[d])))
            if is_update_field_id:
                if d not in is_update_field_id and d not in update_field:
                    update_field.append(d)

        if is_ignore:
            self.sql = "INSERT IGNORE INTO {} ({}) VALUES ('{}')".format(table, ", ".join(fields), "', '".join(values))
        elif is_update_field_id:
            on_duplicate = ["{0} = VALUES({0})".format(uf) for uf in update_field]
            self.sql = "INSERT INTO {} ({}) VALUES ('{}') ON DUPLICATE KEY UPDATE {}".format(table, ", ".join(fields),
                                                                                             "', '".join(values),
                                                                                             ", ".join(on_duplicate))
        else:
            self.sql = "INSERT INTO {} ({}) VALUES ('{}')".format(table, ", ".join(fields), "', '".join(values))

    def insert_many(self, table, data, is_ignore=False):
        self.status = "INSERT"
        if not isinstance(data, dict):
            raise Exception('Data must be dictionary')

        if is_ignore:
            self.sql = "INSERT IGNORE INTO {} ({}) VALUES ".format(table, ", ".join(data['fields']))
        else:
            self.sql = "INSERT INTO {} ({}) VALUES ".format(table, ", ".join(data['fields']))

        values = []
        for value in data['values']:
            new = ['NULL' if v is None else pymysql.escape_string(str(v)) for v in value]
            values.append("('{}')".format("', '".join(new)))

        self.sql = "{} {};".format(self.sql, ", ".join(values))

    def order_by(self, order_by):
        """
        Order By Function
        :param order_by: string
        :return: Set order sql main
        """
        self.q_order = "ORDER BY {}".format(order_by)

    def limit(self, offset=None, limit=None):
        """
        Limit Function
        :param offset: integer
        :param limit: integer
        :return: Set limit and offset sql main
        """
        if offset and limit:
            self.q_limit = "LIMIT {}, {}".format(offset, limit)
        elif limit:
            self.q_limit = "LIMIT {}".format(limit)

    def group_by(self, field):
        """
        Group By Function
        :param field: string
        :return: Set group by sql main
        """
        self.q_group_by = "GROUP BY {}".format(field)

    def execute(self, commit=True, count=False):
        """
        Execute Function
        :param commit: boolean -> True|False
        :param count: boolean -> True|False
        :return: result of execute sql
        """
        sql = ''
        sql_count = ''
        if self.q_where and self.q_where != '':
            self.q_where = "WHERE {}".format(self.q_where)

        if self.status == 'INSERT':
            self.sql = self.sql.replace("'NULL'", 'NULL')

        if self.status in ['QUERY', 'INSERT']:
            sql = self.sql
        elif self.status == 'SELECT':
            sql = "{} {}".format(self.sql, x_str(self.q_join))
            sql_count = "{} {} {}".format(self.sql_count, x_str(self.q_join), x_str(self.q_where))

        if self.status not in ['QUERY', 'INSERT']:
            sql = "{} {} {} {} {}".format(self.sql, x_str(self.q_where), x_str(self.q_group_by), x_str(self.q_order),
                                          x_str(self.q_limit))

        status = self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        lastrowid = self.cursor.lastrowid

        rowscount = None
        if self.status == 'SELECT' and count:
            self.cursor.execute(sql_count)
            rowscount = self.cursor.fetchone()['rowscount']

        if commit:
            self.conn.commit()

        self.reset_var()

        return Return(sql=sql, rows=rows, rowscount=rowscount, status=status, lastrowid=lastrowid)


class Return:
    def __init__(self, sql, rows, rowscount=0, status=0, lastrowid=None):
        self.status = status
        self.sql = sql
        self.data = rows
        self.rowscount = rowscount
        self.fetchall = rows
        self.fetchone = dict()
        self.lastrowid = lastrowid
        if rows:
            self.fetchone = rows[0]
