import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller

        self.desc_entry = None
        self.priority_var = tk.IntVar(value=1)
        self.project_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.search_entry = None
        self.tree = None

        self.create_widgets()

    def create_widgets(self) -> None:
        form_frame = ttk.Frame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="Приоритет:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(form_frame, textvariable=self.priority_var, values=[1, 2, 3]).grid(row=2, column=1, sticky="ew")

        ttk.Label(form_frame, text="Проект:").grid(row=3, column=0, sticky="w")
        project_titles = [p.name for p in self.project_controller.get_all_projects()]
        ttk.Combobox(form_frame, textvariable=self.project_var, values=project_titles).grid(row=3, column=1,
                                                                                            sticky="ew")

        ttk.Label(form_frame, text="Исполнитель:").grid(row=4, column=0, sticky="w")
        user_names = [u.username for u in self.user_controller.get_all_users()]
        ttk.Combobox(form_frame, textvariable=self.user_var, values=user_names).grid(row=4, column=1, sticky="ew")

        ttk.Button(form_frame, text="Добавить задачу", command=self.add_task).grid(
            row=5, column=0, columnspan=2, pady=5
        )

        # Поиск
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(search_frame, text="Поиск:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(search_frame, text="Найти", command=self.refresh_tasks).pack(side="left", padx=5)

        # Таблица задач
        self.tree = ttk.Treeview(
            self,
            columns=("title", "desc", "priority", "status", "project", "assignee"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_tasks(self) -> None:
        # Получаем все задачи
        tasks = self.task_controller.get_all_tasks()

        # Очищаем таблицу
        for row in getattr(self, 'tree', {}).get_children() if hasattr(self, 'tree') else []:
            self.tree.delete(row)

        # Заполняем таблицу
        for task in tasks:
            project = self.project_controller.get_project(task.project_id)
            user = self.user_controller.get_user(task.assignee_id)
            project_title = project.title if project else "—"
            assignee_name = user.username if user else "—"

            self.tree.insert("", "end", iid=task.id, values=(
            task.title, task.description, task.priority, task.status, project_title, assignee_name))

    def add_task(self) -> None:
        title = self.entry_title.get()
        desc = self.entry_description.get()
        priority = int(self.entry_priority.get())

        # Получаем первый проект и первого пользователя
        projects = self.project_controller.get_all_projects()
        users = self.user_controller.get_all_users()
        if not projects or not users:
            messagebox.showerror("Ошибка", "Нет ни одного проекта или пользователя")
            return

        project_id = projects[0].id
        assignee_id = users[0].id

        # Используем метод контроллера
        self.task_controller.add_task(title, desc, priority, datetime.now() + timedelta(days=7), project_id,
                                      assignee_id)
        self.refresh_tasks()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        for task_id in selected:
            task = self.task_controller.get_task(int(task_id))
            if task:
                self.task_controller.delete_task(task)
        self.refresh_tasks()