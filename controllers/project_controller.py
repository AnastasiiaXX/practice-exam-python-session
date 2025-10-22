from models.project import Project
from database.database_manager import DatabaseManager
import sqlite3

class ProjectController:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
        self.db.create_tables()

    def add_project(self, name, description, start_date, end_date) -> int:
        project = Project(name, description, start_date, end_date)
        project_id = self.db.add_project(project)
        return project_id

    def get_project(self, project_id) -> Project | None:
        return self.db.get_project_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        return self.db.get_all_projects()

    def update_project(self, project_id, **kwargs) -> bool:
        try:
            self.db.update_project(project_id, **kwargs)
            return True
        except sqlite3.Error:
            return False

    def delete_project(self, project_id) -> bool:
        try:
            self.db.delete_project(project_id)
            return True
        except sqlite3.Error:
            return False

    def update_project_status(self, project_id, new_status) -> bool:
        try:
            self.db.update_project(project_id, status=new_status)
            return True
        except sqlite3.Error:
            return False

    def get_project_progress(self, project_id) -> float:
        project = self.get_project(project_id)
        if project:
            return project.get_progress()
        return 0.0