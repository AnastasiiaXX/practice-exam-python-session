import os
import tempfile
import pytest
from datetime import datetime

from database.database_manager import DatabaseManager
from models.user import User
from models.project import Project
from models.task import Task

class TestDatabase:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()

    def teardown_method(self):
        self.db_manager.close()
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_tables_created(self):
        """Проверка, что таблицы созданы"""
        db_manager = DatabaseManager("test.db")
        db_manager.create_tables()

        # Получаем список таблиц
        tables = db_manager.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()

        table_names = [t[0] for t in tables]

        assert "users" in table_names
        assert "projects" in table_names
        assert "tasks" in table_names

        db_manager.close()

    def test_add_user_project_task(self):
        """Добавление пользователя, проекта и задачи"""
        user_id = self.db_manager.add_user(User("test", "test@example.com", "developer"))
        project_id = self.db_manager.add_project(Project("Test Project", "Desc", datetime.now(), datetime.now()))
        task_id = self.db_manager.add_task(Task("Test Task", "Desc", 1, datetime.now(), project_id, user_id))

        # Проверка, что записи существуют
        user = self.db_manager.get_user_by_id(user_id)
        project = self.db_manager.get_project_by_id(project_id)
        task = self.db_manager.get_task_by_id(task_id)

        assert user.username == "test"
        assert project.name == "Test Project"
        assert task.title == "Test Task"

    def test_update_user_project_task(self):
        """Обновление записей в БД"""
        user_id = self.db_manager.add_user(User("oldname", "old@example.com", "developer"))
        self.db_manager.update_user(user_id, username="newname", email="new@example.com", role="manager")
        user = self.db_manager.get_user_by_id(user_id)
        assert user.username == "newname"
        assert user.email == "new@example.com"
        assert user.role == "manager"
