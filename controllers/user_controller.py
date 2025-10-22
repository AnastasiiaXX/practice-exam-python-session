from models.user import User
from database.database_manager import DatabaseManager
import sqlite3

class UserController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
        self.db.create_tables()

    def add_user(self, username, email, role) -> int:
        user = User(username, email, role)
        user_id = self.db.add_user(user)
        return user_id

    def get_user(self, user_id) -> User | None:
        return self.db.get_user_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.db.get_all_users()

    def update_user(self, user_id, **kwargs) -> bool:
        try:
            self.db.update_user(user_id, **kwargs)
            return True
        except sqlite3.Error:
            return False

    def delete_user(self, user_id) -> bool:
        try:
            self.db.delete_user(user_id)
            return True
        except sqlite3.Error:
            return False

    def get_user_tasks(self, user_id) -> list:
        return self.db.get_tasks_by_user(user_id)
