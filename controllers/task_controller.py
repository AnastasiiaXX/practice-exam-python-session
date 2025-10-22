from models.task import Task
from database.database_manager import DatabaseManager

class TaskController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
        self.db.create_tables()

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> Task:
        task = Task(title, description, priority, due_date, project_id, assignee_id)
        self.db.add_task(task)
        return task

    def get_task(self, task_id) -> Task | None:
        if isinstance(task_id, Task):
            task_id = task_id.id
        return self.db.get_task_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.db.get_all_tasks()

    def update_task(self, task_id, **kwargs) -> None:
        if isinstance(task_id, Task):
            task_id = task_id.id
        self.db.update_task(task_id, **kwargs)

    def delete_task(self, task_id) -> None:
        if isinstance(task_id, Task):
            task_id = task_id.id
        self.db.delete_task(task_id)

    def search_tasks(self, query) -> list[Task]:
        return self.db.search_tasks(query)

    def update_task_status(self, task_id, new_status) -> None:
        if isinstance(task_id, Task):
            task_id = task_id.id
        self.db.update_task(task_id, status=new_status)

    def get_overdue_tasks(self) -> list[Task]:
        all_tasks = self.db.get_all_tasks()
        return [task for task in all_tasks if task.is_overdue()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        return self.db.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id) -> list[Task]:
        return self.db.get_tasks_by_user(user_id)
