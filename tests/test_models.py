import os
import tempfile
import pytest
from datetime import datetime, timedelta
from models.project import Project
from models.user import User
from models.task import Task
from database.database_manager import DatabaseManager

class TestProjectModel:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()

    def teardown_method(self):
        self.db_manager.close()
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_project_creation_valid(self):
        start = datetime.now()
        end = start + timedelta(days=5)
        project = Project("Test", "Desc", start, end)
        assert project.name == "Test"
        assert project.status == "active"

    def test_project_update_status_valid(self):
        start = datetime.now()
        end = start + timedelta(days=5)
        project = Project("Test", "Desc", start, end)
        project.update_status("completed")
        assert project.status == "completed"

    def test_project_update_status_invalid(self):
        start = datetime.now()
        end = start + timedelta(days=5)
        project = Project("Test", "Desc", start, end)
        with pytest.raises(ValueError):
            project.update_status("unknown")

    def test_project_progress_boundaries(self):
        # Проект в будущем — прогресс 0
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(days=5)
        project = Project("Future", "Desc", start, end)
        assert project.get_progress() == 0.0

        # Проект в прошлом — прогресс 100
        start = datetime.now() - timedelta(days=10)
        end = start + timedelta(days=5)
        project = Project("Past", "Desc", start, end)
        assert project.get_progress() == 100.0

    def test_project_to_dict(self):
        start = datetime.now()
        end = start + timedelta(days=5)
        project = Project("Test", "Desc", start, end)
        d = project.to_dict()
        assert d["name"] == "Test"
        assert d["status"] == "active"
        assert "start_date" in d
        assert "end_date" in d

class TestUserModel:
    def test_user_creation_valid(self):
        """Создание пользователя с валидными данными"""
        self.user = User("john", "john@example.com", "developer")
        assert self.user.username == "john"
        assert self.user.email == "john@example.com"
        assert self.user.role == "developer"
        assert isinstance(self.user.registration_date, datetime)
        assert self.user.id is None

    def test_user_creation_invalid_email(self):
        """Проверка валидации email"""
        with pytest.raises(ValueError):
            self.user = User("john", "invalid-email", "developer")

    def test_user_creation_invalid_role(self):
        """Проверка валидации роли"""
        with pytest.raises(ValueError):
            self.user = User("john", "john@example.com", "unknown")

    def test_user_update_info_username_email_role(self):
        """Обновление информации пользователя"""
        self.user = User("john", "john@example.com", "developer")
        self.user.update_info(username="jane", email="jane@example.com", role="manager")
        assert self.user.username == "jane"
        assert self.user.email == "jane@example.com"
        assert self.user.role == "manager"


    def test_user_update_info_partial(self):
        """Обновление только части данных"""
        self.user = User("john", "john@example.com", "developer")
        self.user.update_info(username="newname")
        assert self.user.username == "newname"
        assert self.user.email == "john@example.com"
        assert self.user.role == "developer"

    def test_user_to_dict(self):
        """Проверка метода to_dict"""
        self.user = User("john", "john@example.com", "developer")
        d = self.user.to_dict()
        assert d["username"] == "john"
        assert d["email"] == "john@example.com"
        assert d["role"] == "developer"
        assert "registration_date" in d
        assert d["id"] is None


class TestTaskModel:
    def test_task_creation_valid(self):
        """Создание задачи с валидными данными"""
        due = datetime.now() + timedelta(days=5)
        self.task = Task("Task 1", "Desc", 2, due, 1, 1)
        assert self.task.title == "Task 1"
        assert self.task.priority == 2
        assert self.task.status == "pending"
        assert self.task.project_id == 1
        assert self.task.assignee_id == 1
        assert isinstance(self.task.due_date, datetime)

    def test_task_creation_empty_title(self):
        """Проверка валидации пустого title"""
        due = datetime.now() + timedelta(days=5)
        with pytest.raises(ValueError):
            self.task = Task("", "Desc", 2, due, 1, 1)


    def test_task_creation_invalid_due_date(self):
        """Проверка типа due_date"""
        with pytest.raises(TypeError):
            self.task = Task("Task", "Desc", 2, "2025-01-01", 1, 1)


    def test_task_update_status_invalid(self):
        """Обновление статуса задачи на недопустимый"""
        due = datetime.now() + timedelta(days=5)
        self.task = Task("Task", "Desc", 2, due, 1, 1)
        with pytest.raises(ValueError):
            self.task.update_status("done")

    def test_task_is_overdue_future(self):
        """Задача не просрочена"""
        due = datetime.now() + timedelta(days=5)
        self.task = Task("Task", "Desc", 2, due, 1, 1)
        assert self.task.is_overdue() is False

    def test_task_is_overdue_past(self):
        """Задача просрочена"""
        due = datetime.now() - timedelta(days=1)
        self.task = Task("Task", "Desc", 2, due, 1, 1)
        assert self.task.is_overdue() is True

    def test_task_to_dict(self):
        """Проверка метода to_dict"""
        due = datetime.now() + timedelta(days=5)
        self.task = Task("Task", "Desc", 2, due, 1, 1)
        d = self.task.to_dict()
        assert d["title"] == "Task"
        assert d["priority"] == 2
        assert d["status"] == "pending"
        assert d["project_id"] == 1
        assert d["assignee_id"] == 1
        assert "due_date" in d
        assert d["id"] is None
