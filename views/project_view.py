import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller

        # Поля ввода
        self.name_entry = None
        self.desc_entry = None
        self.start_entry = None
        self.end_entry = None
        self.tree = None

        self.create_widgets()

    def create_widgets(self) -> None:
        # Форма добавления/редактирования
        form_frame = ttk.Frame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="Дата начала (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.start_entry = ttk.Entry(form_frame)
        self.start_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(form_frame, text="Дата окончания (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.end_entry = ttk.Entry(form_frame)
        self.end_entry.grid(row=3, column=1, sticky="ew")

        ttk.Button(form_frame, text="Добавить проект", command=self.add_project).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        # Таблица проектов
        self.tree = ttk.Treeview(
            self,
            columns=("name", "desc", "start", "end", "progress"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_projects()

    def refresh_projects(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
        for project in self.project_controller.get_all_projects():
            progress = f"{self.project_controller.get_project_progress(project.id):.0f}%"
            self.tree.insert("", "end", values=(
                project.name,
                project.description,
                project.start_date,
                project.end_date,
                progress
            ))

    def add_project(self) -> None:
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        start_date_str = self.start_entry.get()
        end_date_str = self.end_entry.get()

        if not name or not start_date_str or not end_date_str:
            messagebox.showwarning("Ошибка", "Заполните обязательные поля")
            return

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
            return

        self.project_controller.add_project(name, desc, start_date, end_date)
        self.refresh_projects()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите проект для удаления")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            project_name = values[0]
            for project in self.project_controller.get_all_projects():
                if project.name == project_name:
                    self.project_controller.delete_project(project.id)
                    break
        self.refresh_projects()