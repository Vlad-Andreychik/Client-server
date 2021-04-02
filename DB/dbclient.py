import sqlite3


class DB:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def add_user(self, login, password):
        params = (login, password)
        self.cursor.execute("INSERT INTO Users VALUES (?, ?)", params)
        self.db.commit()

    def exist_login(self, login):
        self.cursor.execute(f"""SELECT * FROM Users WHERE login = '{login}'""")
        return self.cursor.fetchall()

    def select_for_sign_in(self, login):
        self.cursor.execute(f"""SELECT password FROM Users WHERE login='{login}'""")
        return self.cursor.fetchone()[0]
