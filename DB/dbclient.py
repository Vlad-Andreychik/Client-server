import sqlite3


class DB:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def insert(self, value_1, value_2):
        params = (value_1, value_2)
        self.cursor.execute("INSERT INTO Users VALUES (?, ?)", params)
        self.db.commit()

    def select(self, query):
        self.cursor.execute(f"""SELECT '{query}' FROM Users""")
        return self.cursor.fetchall()

    def select_where(self, select_query, where_parameter, where_query):
        self.cursor.execute(f"""SELECT {select_query} FROM Users WHERE {where_parameter}='{where_query}' """)
        return self.cursor.fetchall()

    def disconnect(self):
        self.db.close()
