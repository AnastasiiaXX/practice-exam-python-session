import tkinter as tk
from tkinter import ttk, messagebox

ROLES = ['admin', 'manager', 'developer']

class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller

        # Поля ввода
        self.username_entry = None
        self.email_entry = None
        self.role_entry = None
        self.tree = None

        self.create_widgets()

    def create_widgets(self) -> None:
        # Форма добавления
        form_frame = ttk.Frame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Имя пользователя:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="Роль:").grid(row=2, column=0, sticky="w")
        self.role_entry = ttk.Combobox(form_frame, values=ROLES, state="readonly")  # ✅ теперь выпадающий список
        self.role_entry.grid(row=2, column=1, sticky="ew")
        self.role_entry.set(ROLES[0])

        add_btn = ttk.Button(form_frame, text="Добавить", command=self.add_user)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        delete_btn = ttk.Button(form_frame, text="Удалить выбранных", command=self.delete_selected)
        delete_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица пользователей
        self.tree = ttk.Treeview(self, columns=("id", "username", "email", "role"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_users()

    def refresh_users(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)

        users = self.user_controller.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(user.id, user.username, user.email, user.role))

    def add_user(self) -> None:
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_entry.get().strip()

        if not username or not email or not role:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        self.user_controller.add_user(username, email, role)
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.refresh_users()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите пользователя для удаления!")
            return

        for item in selected:
            values = self.tree.item(item, "values")
            user_id = values[0]
            self.user_controller.delete_user(user_id)

        self.refresh_users()