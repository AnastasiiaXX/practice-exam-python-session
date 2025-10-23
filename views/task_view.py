import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta

allowed_statuses = ['pending', 'in_progress', 'completed']

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
        self.status_var = tk.StringVar(value="")

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
        ttk.Combobox(form_frame, textvariable=self.project_var, values=project_titles).grid(row=3, column=1, sticky="ew")

        ttk.Label(form_frame, text="Исполнитель:").grid(row=4, column=0, sticky="w")

        user_names = [u.username for u in self.user_controller.get_all_users()]
        ttk.Combobox(form_frame, textvariable=self.user_var, values=user_names).grid(row=4, column=1, sticky="ew")

        # Кнопки действий
        ttk.Button(form_frame, text="Добавить задачу", command=self.add_task).grid(
            row=5, column=0, columnspan=2, pady=5
        )
        ttk.Button(form_frame, text="Редактировать выбранную", command=self.edit_selected).grid(
            row=6, column=0, columnspan=2, pady=5
        )
        ttk.Button(form_frame, text="Удалить выбранные", command=self.delete_selected).grid(
            row=7, column=0, columnspan=2, pady=5
        )

        # Поиск
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(search_frame, text="Поиск:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(search_frame, text="Найти", command=self.refresh_tasks).pack(side="left", padx=5)

        ttk.Label(search_frame, text="Статус:").pack(side="left", padx=(10, 0))
        ttk.Combobox(search_frame, textvariable=self.status_var, values=[""] + allowed_statuses, width=12).pack(
            side="left")

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
        tasks = self.task_controller.get_all_tasks()

        # Фильтры поиска
        query = self.search_entry.get().strip().lower() if self.search_entry else ""
        status_filter_value = self.status_var.get() if self.status_var else ""
        priority_filter_value = getattr(self, "priority_var_filter", None)
        if priority_filter_value:
            priority_filter_value = priority_filter_value.get()
        else:
            priority_filter_value = 0

        filtered_tasks = []
        for task in tasks:
            # Поиск по названию и описанию
            if query and query not in task.title.lower() and query not in task.description.lower():
                continue

            # Фильтр по статусу
            if status_filter_value and task.status != status_filter_value:
                continue

            # Фильтр по приоритету
            if priority_filter_value and task.priority != priority_filter_value:
                continue

            filtered_tasks.append(task)

        # Очищаем таблицу
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Заполняем таблицу
        for task in filtered_tasks:
            project = self.project_controller.get_project(task.project_id)
            user = self.user_controller.get_user(task.assignee_id)
            project_name = project.name if project else "—"
            assignee_name = user.username if user else "—"

            self.tree.insert("", "end", iid=task.id, values=(
                task.title, task.description, task.priority, task.status, project_name, assignee_name
            ))

    def add_task(self) -> None:
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        priority = int(self.priority_var.get())

        if not title:
            messagebox.showerror("Ошибка", "Введите название задачи!")
            return

        projects = self.project_controller.get_all_projects()
        users = self.user_controller.get_all_users()

        if not projects or not users:
            messagebox.showerror("Ошибка", "Нет доступных проектов или пользователей")
            return

        project = next((p for p in projects if p.name == self.project_var.get()), projects[0])
        user = next((u for u in users if u.username == self.user_var.get()), users[0])

        due_date = datetime.now() + timedelta(days=7)
        self.task_controller.add_task(title, desc, priority, due_date, project.id, user.id)
        messagebox.showinfo("Успех", "Задача добавлена")
        self.refresh_tasks()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")
            return

        for item in selected:
            task_id = int(item)
            task = self.task_controller.get_task(task_id)
            if task:
                self.task_controller.delete_task(task)
        self.refresh_tasks()
        messagebox.showinfo("Успех", "Выбранные задачи успешно удалены")

    def edit_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для редактирования")
            return

        task_id = int(selected[0])
        task = self.task_controller.get_task(task_id)

        if not task:
            messagebox.showerror("Ошибка", "Не удалось найти задачу")
            return

        # Простое окно ввода новых данных
        new_title = simpledialog.askstring("Редактировать задачу", "Новое название:", initialvalue=task.title)
        new_desc = simpledialog.askstring("Редактировать задачу", "Новое описание:", initialvalue=task.description)

        if new_title and new_desc:
            task.title = new_title
            task.description = new_desc
            self.task_controller.update_task(task.id, title=new_title, description=new_desc)
            self.refresh_tasks()
            messagebox.showinfo("Успех", "Задача обновлена")
