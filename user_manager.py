import uuid
import sqlite3

class UserManager:
    def __init__(self, db):
        self.db = db

    def get_user(self, username):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            return cur.fetchone()

    def get_user_by_id(self, uid):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
            return cur.fetchone()

    def create_user(self, username, password):
        api_key = str(uuid.uuid4())
        try:
            with self.db.connect() as con:
                con.execute("INSERT INTO users (username, password, api_key) VALUES (?, ?, ?)",
                            (username, password, api_key))
            return True, None
        except sqlite3.IntegrityError:
            return False, "Пользователь уже существует"
