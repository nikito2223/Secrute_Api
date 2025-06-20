import sqlite3

class Database:
    DB_PATH = "db.sqlite3"

    def __init__(self):
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.DB_PATH)

    def init_db(self):
        with self.connect() as con:
            cur = con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    api_key TEXT
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS access (
                    user_id INTEGER,
                    program_name TEXT,
                    enabled INTEGER DEFAULT 0
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS flags (
                    user_id INTEGER,
                    program_name TEXT,
                    flag_name TEXT,
                    flag_value INTEGER DEFAULT 0,
                    UNIQUE(user_id, program_name, flag_name)
                )
            ''')
