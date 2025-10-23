# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.project_view import ProjectView
from views.task_view import TaskView
from views.user_view import UserView
from controllers.task_controller import TaskController


class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("1000x600")

        # Создаём вкладки
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Вкладка задач
        self.task_view = TaskView(
            self,
            task_controller,
            project_controller,
            user_controller
        )
        self.tab_control.add(self.task_view, text="Задачи")

        # Вкладка проектов
        self.project_view = ProjectView(
            self,
            project_controller,
            task_controller
        )
        self.tab_control.add(self.project_view, text="Проекты")

        # Вкладка пользователей
        self.user_view = UserView(
            self,
            user_controller,
        )
        self.tab_control.add(self.user_view, text="Пользователи")

