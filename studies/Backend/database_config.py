import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # Permite conexões em múltiplas threads
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    login TEXT NOT NULL,
                    start_date TEXT NOT NULL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    photo BLOB,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

    def close(self):
        self.conn.close()
