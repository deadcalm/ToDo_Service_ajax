import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from ..entities import User, Todo


db = sqlite3.connect(Path(__file__).parent / '..' / '..' / 'db' / 'database.sqlite', check_same_thread=False)

class Storage: 
    @staticmethod
    def add_user(user):
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user.email, generate_password_hash(user.password)))
        db.commit()
    
    @staticmethod
    def get_user_by_email_and_password(email, password):
        user_data = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], password):
            return User(*user_data)
        else:
            return None
    

    @staticmethod
    def get_user_by_id(id):
        user_data = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None

    @staticmethod
    def is_email_used(email):
        user_data = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if user_data:
            return True
        return False

    @staticmethod
    def get_todos_by_user_id(user_id):
        rows = db.execute('SELECT * FROM todos WHERE user_id = ?', (user_id,)).fetchall()
        return [Todo(*row) for row in rows]
    
    @staticmethod
    def create_todo(title, description, user_id):
        todo_id = db.execute('INSERT INTO todos (title, description, user_id) VALUES (?, ?, ?)', (title, description, user_id)).lastrowid
        db.commit()
        return Todo(todo_id, title, description, user_id, False)

    @staticmethod
    def delete_todo(todo_id, user_id):
        db.execute('DELETE FROM todos WHERE id = ? AND user_id = ?', (todo_id, user_id)).lastrowid
        db.commit()
