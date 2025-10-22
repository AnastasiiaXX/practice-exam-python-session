import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title VARCHAR(30) NOT NULL,
                        description TEXT,
                        priority INTEGER NOT NULL,
                        status VARCHAR(20) NOT NULL,
                        due_date DATETIME NOT NULL,
                        project_id INTEGER,
                        assignee_id INTEGER
                    )
                ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS projects (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(30) NOT NULL,
                                description TEXT,
                                start_date DATETIME NOT NULL,
                                end_date DATETIME NOT NULL,
                                status VARCHAR(20) NOT NULL
                            )
                        ''')
        self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        username VARCHAR(50) NOT NULL,
                                        email VARCHAR(55) NOT NULL,
                                        role VARCHAR(25) NOT NULL,
                                        registration_date DATETIME NOT NULL
                                    )
                                ''')
        self.conn.commit()

    def add_task(self, task: Task) -> int:
        self.cursor.execute(
            '''
            INSERT INTO tasks (title, description, priority, 
            status, due_date, project_id, assignee_id) VALUES
            (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date.strftime("%Y-%m-%d %H:%M:%S"),
                task.project_id,
                task.assignee_id
            ))
        self.conn.commit()
        task.id = self.cursor.lastrowid

    def get_task_by_id(self, task_id) -> Task | None:
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = self.cursor.fetchone()
        if row:
            return Task(
                title=row[1],
                description=row[2],
                priority=row[3],
                due_date=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
                project_id=row[6],
                assignee_id=row[7]
            )
            task.id = row[0]
            task.status = row[4]
            return task
        return None

    def get_all_tasks(self) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(
                title=row[1],
                description=row[2],
                priority=row[3],
                due_date=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
                project_id=row[6],
                assignee_id=row[7]
            )
            task.id = row[0]
            task.status = row[4]
            tasks.append(task)
        return tasks

    def update_task(self, task_id, **kwargs) -> bool:
        fields = []
        values = []

        for key, value in kwargs.items():
            if key == 'due_date' and isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            fields.append(f'{key} = ?')
            values.append(value)

        values.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete_task(self, task_id) -> bool:
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def search_tasks(self, query) -> list[Task]:
        self.cursor.execute(
            '''
            SELECT * FROM tasks
            WHERE title LIKE ?
            ''',
            (f'%{query}%',)
        )
        rows = self.cursor.fetchall()
        results = []
        for row in rows:
            task = Task(
                title=row[1],
                description=row[2],
                priority=row[3],
                due_date=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
                project_id=row[6],
                assignee_id=row[7]
            )
            task.id = row[0]
            task.status = row[4]
            results.append(task)
        return results

    def get_tasks_by_project(self, project_id) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = self.cursor.fetchall()
        return [
            Task(
                title=row[1],
                description=row[2],
                priority=row[3],
                status=row[4],
                due_date=row[5],
                project_id=row[6],
                assignee_id=row[7]
            )
            for row in rows
        ]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        self.cursor.execute('SELECT * FROM tasks WHERE assignee_id = ?', (user_id,))
        rows = self.cursor.fetchall()
        return [
            Task(
                title=row[1],
                description=row[2],
                priority=row[3],
                status=row[4],
                due_date=row[5],
                project_id=row[6],
                assignee_id=row[7]
            )
            for row in rows
        ]

    def add_project(self, project: Project) -> int:
        self.cursor.execute(
            '''
            INSERT INTO projects (name, description, start_date, end_date, status) 
            VALUES (?, ?, ?, ?, ?)
            ''', (
                project.name,
                project.description,
                project.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                project.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                project.status,
            ))
        self.conn.commit()
        project.id = self.cursor.lastrowid


    def get_project_by_id(self, project_id) -> Project | None:
        self.cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = self.cursor.fetchone()
        if row:
            return Project(
                name=row[1],
                description=row[2],
                start_date=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                end_date=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),
                status=row[5],
            )
        return None

    def get_all_projects(self) -> list[Project]:
        self.cursor.execute('SELECT * FROM projects')
        rows = self.cursor.fetchall()
        projects = []
        for row in rows:
            project = Project(
                name=row[1],
                description=row[2],
                start_date=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                end_date=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),
                status=row[5],
            )
            project.id = row[0]
            projects.append(project)
        return projects

    def update_project(self, project_id, **kwargs) -> bool:
        fields = []
        values = []

        for key, value in kwargs.items():
            if (key == 'start_date' or key == 'end_date') and isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            fields.append(f'{key} = ?')
            values.append(value)

        values.append(project_id)
        sql = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete_project(self, project_id) -> bool:
        self.cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.conn.commit()

    def add_user(self, user: User) -> int:
        self.cursor.execute(
            '''
            INSERT INTO users (username, email, role, registration_date) 
            VALUES (?, ?, ?, ?)
            ''', (
                user.username,
                user.email,
                user.role,
                user.registration_date.strftime("%Y-%m-%d %H:%M:%S")
            ))
        self.conn.commit()
        user.id = self.cursor.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()
        if row:
            user = User(
                username=row[1],
                email=row[2],
                role=row[3],
            )
            user.id = row[0]
            user.registration_date = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            return user
        return None

    def get_all_users(self) -> list[User]:
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            user = User(
                username=row[1],
                email=row[2],
                role=row[3],
            )
            user.id = row[0]
            user.registration_date = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            users.append(user)
        return users

    def update_user(self, user_id, **kwargs) -> bool:
        fields = []
        values = []

        for key, value in kwargs.items():
            if key == 'registration_date' and isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            fields.append(f'{key} = ?')
            values.append(value)

        values.append(user_id)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete_user(self, user_id) -> bool:
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
