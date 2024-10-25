from database_config import Database
from datetime import datetime


class UserOperations:
    def __init__(self):
        self.db = Database()


    def add_user(self, username, login, start_date=None):
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        with self.db.conn:
            self.db.conn.execute('''
                INSERT INTO users (username, login, start_date)
                VALUES (?, ?, ?)
            ''', (username, login, start_date))



    def get_user_id(self, username):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
        

    def get_user(self, user_id):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

    def add_photo(self, user_id, photo_data):
        if self.get_user(user_id):
            with self.db.conn:
                self.db.conn.execute('''
                    INSERT INTO photos (user_id, photo)
                    VALUES (?, ?)
                ''', (user_id, photo_data))
               
                
        else:
            print(f"Usuário com ID {user_id} não encontrado!")

    def get_photos(self, user_id):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

    def close(self):
        self.db.close()
