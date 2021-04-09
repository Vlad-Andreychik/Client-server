"""Module of database that provides connection and working with database"""

import sqlite3


class DB:
    """
    Class that provides connection and working with database
    """
    def __init__(self, path):
        """
        Constructor init takes 1 parameter and makes connection with database
        :param path: a path to database
        """
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def insert(self, value_1, value_2):
        """
        Method that inserts a new row in table Users
        :param value_1: value for first column
        :param value_2: value for second column
        """
        params = (value_1, value_2)
        self.cursor.execute("INSERT INTO Users VALUES (?, ?)", params)
        self.db.commit()

    def select(self, query):
        """
        Method that selects columns in table Users
        :param query: query for select
        :return: all matching columns
        """
        self.cursor.execute(f"""SELECT '{query}' FROM Users""")
        return self.cursor.fetchall()

    def select_where(self, select_query, where_parameter, where_query):
        """
        Method that selects columns using an additional parameter WHERE in table users
        :param select_query: query for select
        :param where_parameter: what column you would define
        :param where_query: what query for this column
        :return: all matching columns
        """
        self.cursor.execute(f"""SELECT {select_query} FROM Users WHERE {where_parameter}='{where_query}' """)
        return self.cursor.fetchall()

    def disconnect(self):
        """
        Method that disconnects from database
        """
        self.db.close()
