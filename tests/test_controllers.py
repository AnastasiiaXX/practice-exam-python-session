import os
import tempfile
from datetime import datetime, timedelta

from database.database_manager import DatabaseManager
from controllers.project_controller import ProjectController
from controllers.task_controller import TaskController
from controllers.user_controller import UserController
from models.user import User
from models.task import Task
from models.project import Project

"""Тесты для всех контроллеров уже были написаны в шаблоне для задания"""

class TestProjectController:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        self.controller = ProjectController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_add_project(self):
        """Тест добавления проекта"""
        project_id = self.controller.add_project(
            "Новый проект",
            "Описание нового проекта",
            datetime.now(),
            datetime.now() + timedelta(days=30)
        )

        assert project_id is not None
        assert isinstance(project_id, int)

        # Проверяем, что проект действительно добавлен
        project = self.controller.get_project(project_id)
        assert project.name == "Новый проект"
        assert project.description == "Описание нового проекта"
        assert project.status == "active"

    def test_get_project(self):
        """Тест получения проекта по ID"""
        project_id = self.controller.add_project(
            "Проект для получения",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=30)
        )

        project = self.controller.get_project(project_id)
        assert project is not None
        assert project.name == "Проект для получения"
        assert project.status == "active"

    def test_get_all_projects(self):
        """Тест получения всех проектов"""
        # Добавляем несколько проектов
        self.controller.add_project("Проект 1", "Описание 1", datetime.now(), datetime.now() + timedelta(days=10))
        self.controller.add_project("Проект 2", "Описание 2", datetime.now(), datetime.now() + timedelta(days=20))

        projects = self.controller.get_all_projects()
        assert len(projects) >= 2

        # Проверяем, что все проекты имеют необходимые атрибуты
        for project in projects:
            assert hasattr(project, "id")
            assert hasattr(project, "name")
            assert hasattr(project, "status")

    def test_update_project(self):
        """Тест обновления проекта"""
        project_id = self.controller.add_project(
            "Старое название",
            "Старое описание",
            datetime.now(),
            datetime.now() + timedelta(days=10)
        )

        # Обновляем проект
        self.controller.update_project(
            project_id,
            name="Новое название",
            description="Новое описание"
        )

        # Проверяем изменения
        project = self.controller.get_project(project_id)
        assert project.name == "Новое название"
        assert project.description == "Новое описание"

    def test_delete_project(self):
        """Тест удаления проекта"""
        project_id = self.controller.add_project(
            "Проект для удаления",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10)
        )

        # Удаляем проект
        self.controller.delete_project(project_id)

        # Проверяем, что проект удален
        project = self.controller.get_project(project_id)
        assert project is None

    def test_update_project_status(self):
        """Тест обновления статуса проекта"""
        project_id = self.controller.add_project(
            "Проект для смены статуса",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10)
        )

        # Обновляем статус
        self.controller.update_project_status(project_id, "completed")

        # Проверяем изменения
        project = self.controller.get_project(project_id)
        assert project.status == "completed"

    def test_get_project_progress(self):
        """Тест получения прогресса проекта"""
        project_id = self.controller.add_project(
            "Проект для прогресса",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=10)
        )

        # Создаем задачи для проекта
        task_controller = TaskController(self.db_manager)
        user_id = self.db_manager.add_user(User("test", "test@example.com", "developer"))

        # Добавляем задачи с разными статусами
        task_controller.add_task("Задача 1", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)
        task_controller.add_task("Задача 2", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)

        # Помечаем одну задачу как выполненную
        tasks = task_controller.get_tasks_by_project(project_id)
        if tasks:
            task_controller.update_task_status(tasks[0].id, "completed")

        progress = self.controller.get_project_progress(project_id)
        assert isinstance(progress, float)
        assert 0 <= progress <= 100


class TestTaskController:
    """Тесты для TaskController"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        self.controller = TaskController(self.db_manager)

        # Создаем тестовые проекты и пользователей
        self.project_id = self.db_manager.add_project(
            Project("Тестовый проект", "Описание проекта", datetime.now(), datetime.now() + timedelta(days=30))
        )
        self.user_id = self.db_manager.add_user(
            User("test_user", "test@example.com", "developer")
        )

    def teardown_method(self):
        self.db_manager.close()
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_add_task(self):
        """Тест добавления задачи"""
        task = self.controller.add_task(
            "Test task",
            "Test task description",
            1,
            datetime.now() + timedelta(days=7),
            self.project_id,
            self.user_id
        )

        assert task is not None
        assert isinstance(task, Task)
        assert task.id is not None

        # Проверяем, что задача добавлена
        assert task.title == "Test task"
        assert task.description == "Test task description"
        assert task.priority == 1

    def test_get_task(self):
        """Тест получения задачи по ID"""
        task_id = self.controller.add_task(
            "Задача для получения",
            "Описание",
            2,
            datetime.now() + timedelta(days=5),
            self.project_id,
            self.user_id
        )

        task = self.controller.get_task(task_id)
        assert task is not None
        assert task.title == "Задача для получения"
        assert task.status == "pending"

    def test_get_all_tasks(self):
        """Тест получения всех задач"""
        # Добавляем несколько задач
        self.controller.add_task("Задача 1", "Описание 1", 1, datetime.now() + timedelta(days=1), self.project_id,
                                 self.user_id)
        self.controller.add_task("Задача 2", "Описание 2", 2, datetime.now() + timedelta(days=2), self.project_id,
                                 self.user_id)

        tasks = self.controller.get_all_tasks()
        assert len(tasks) >= 2

        # Проверяем, что все задачи имеют необходимые атрибуты
        for task in tasks:
            assert hasattr(task, "id")
            assert hasattr(task, "title")
            assert hasattr(task, "status")

    def test_update_task(self):
        """Тест обновления задачи"""
        task_id = self.controller.add_task(
            "Старое название",
            "Старое описание",
            1,
            datetime.now() + timedelta(days=3),
            self.project_id,
            self.user_id
        )

        # Обновляем задачу
        self.controller.update_task(
            task_id,
            title="Новое название",
            description="Новое описание",
            priority=3
        )

        # Проверяем изменения
        task = self.controller.get_task(task_id)
        assert task.title == "Новое название"
        assert task.description == "Новое описание"
        assert task.priority == 3

    def test_delete_task(self):
        """Тест удаления задачи"""
        task_id = self.controller.add_task(
            "Задача для удаления",
            "Описание",
            1,
            datetime.now() + timedelta(days=1),
            self.project_id,
            self.user_id
        )

        # Удаляем задачу
        self.controller.delete_task(task_id)

        # Проверяем, что задача удалена
        task = self.controller.get_task(task_id)
        assert task is None

    def test_search_tasks(self):
        """Тест поиска задач"""
        self.controller.add_task("Важная задача", "Срочное выполнение", 1, datetime.now() + timedelta(days=1),
                                 self.project_id, self.user_id)
        self.controller.add_task("Обычная задача", "Плановое выполнение", 2, datetime.now() + timedelta(days=2),
                                 self.project_id, self.user_id)

        # Поиск по названию
        results = self.controller.search_tasks("Важная")
        assert len(results) >= 1

        # Поиск по описанию
        results = self.controller.search_tasks("Срочное")
        assert len(results) >= 1

    def test_update_task_status(self):
        """Тест обновления статуса задачи"""
        task_id = self.controller.add_task(
            "Задача для смены статуса",
            "Описание",
            1,
            datetime.now() + timedelta(days=1),
            self.project_id,
            self.user_id
        )

        # Обновляем статус
        self.controller.update_task_status(task_id, "in_progress")

        # Проверяем изменения
        task = self.controller.get_task(task_id)
        assert task.status == "in_progress"

        # Обновляем на завершенный
        self.controller.update_task_status(task_id, "completed")
        task = self.controller.get_task(task_id)
        assert task.status == "completed"

    def test_get_overdue_tasks(self):
        """Тест получения просроченных задач"""
        # Создаем просроченную задачу
        task_id = self.controller.add_task(
            "Просроченная задача",
            "Описание",
            1,
            datetime.now() - timedelta(days=1),  # Вчерашний срок
            self.project_id,
            self.user_id
        )

        overdue_tasks = self.controller.get_overdue_tasks()
        assert len(overdue_tasks) >= 1

        for task in overdue_tasks:
            assert task.is_overdue() == True

    def test_get_tasks_by_project(self):
        """Тест получения задач проекта"""
        # Создаем второй проект
        project2_id = self.db_manager.add_project(
            Project("Второй проект", "Описание", datetime.now(), datetime.now() + timedelta(days=30))
        )

        # Добавляем задачи в разные проекты
        self.controller.add_task("Задача в проекте 1", "Описание", 1, datetime.now() + timedelta(days=1),
                                 self.project_id, self.user_id)
        self.controller.add_task("Задача в проекте 2", "Описание", 1, datetime.now() + timedelta(days=1), project2_id,
                                 self.user_id)

        tasks = self.controller.get_tasks_by_project(self.project_id)
        assert len(tasks) >= 1

        for task in tasks:
            assert task.project_id == self.project_id

    def test_get_tasks_by_user(self):
        """Тест получения задач пользователя"""
        # Создаем второго пользователя
        user2_id = self.db_manager.add_user(
            User("user2", "user2@example.com", "developer")
        )

        # Добавляем задачи разным пользователям
        self.controller.add_task("Задача пользователя 1", "Описание", 1, datetime.now() + timedelta(days=1),
                                 self.project_id, self.user_id)
        self.controller.add_task("Задача пользователя 2", "Описание", 1, datetime.now() + timedelta(days=1),
                                 self.project_id, user2_id)

        tasks = self.controller.get_tasks_by_user(self.user_id)
        assert len(tasks) >= 1

        for task in tasks:
            assert task.assignee_id == self.user_id

class TestUserController:
    """Тесты для UserController"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        self.controller = UserController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_add_user(self):
        """Тест добавления пользователя"""
        user_id = self.controller.add_user(
            "new_user",
            "new_user@example.com",
            "developer"
        )

        assert user_id is not None
        assert isinstance(user_id, int)

        # Проверяем, что пользователь действительно добавлен
        user = self.controller.get_user(user_id)
        assert user.username == "new_user"
        assert user.email == "new_user@example.com"
        assert user.role == "developer"

    def test_get_user(self):
        """Тест получения пользователя по ID"""
        user_id = self.controller.add_user(
            "user_for_get",
            "user@example.com",
            "manager"
        )

        user = self.controller.get_user(user_id)
        assert user is not None
        assert user.username == "user_for_get"
        assert user.role == "manager"

    def test_get_all_users(self):
        """Тест получения всех пользователей"""
        # Добавляем несколько пользователей
        self.controller.add_user("user1", "user1@example.com", "developer")
        self.controller.add_user("user2", "user2@example.com", "manager")

        users = self.controller.get_all_users()
        assert len(users) >= 2

        # Проверяем, что все пользователи имеют необходимые атрибуты
        for user in users:
            assert hasattr(user, "id")
            assert hasattr(user, "username")
            assert hasattr(user, "role")

    def test_update_user(self):
        """Тест обновления пользователя"""
        user_id = self.controller.add_user(
            "old_username",
            "old@example.com",
            "developer"
        )

        # Обновляем пользователя
        self.controller.update_user(
            user_id,
            username="new_username",
            email="new@example.com",
            role="manager"
        )

        # Проверяем изменения
        user = self.controller.get_user(user_id)
        assert user.username == "new_username"
        assert user.email == "new@example.com"
        assert user.role == "manager"

    def test_delete_user(self):
        """Тест удаления пользователя"""
        user_id = self.controller.add_user(
            "user_for_delete",
            "delete@example.com",
            "developer"
        )

        # Удаляем пользователя
        self.controller.delete_user(user_id)

        # Проверяем, что пользователь удален
        user = self.controller.get_user(user_id)
        assert user is None

    def test_get_user_tasks(self):
        """Тест получения задач пользователя"""
        user_id = self.controller.add_user("task_user", "task@example.com", "developer")

        # Создаем проект и задачи
        project_controller = ProjectController(self.db_manager)
        project_id = project_controller.add_project(
            "Проект для задач", "Описание", datetime.now(), datetime.now() + timedelta(days=10)
        )

        task_controller = TaskController(self.db_manager)
        task_controller.add_task("Задача 1", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)
        task_controller.add_task("Задача 2", "Описание", 1, datetime.now() + timedelta(days=1), project_id, user_id)

        tasks = self.controller.get_user_tasks(user_id)
        assert isinstance(tasks, list)
        assert len(tasks) >= 2

        for task in tasks:
            assert task.assignee_id == user_id