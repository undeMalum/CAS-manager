import tkinter as tk
from tkinter import ttk

from src.students_display.db import fetching_students_from_db


class StudentsView(ttk.LabelFrame):
    def __init__(self, root):
        super().__init__(root)

        self.scrollbar = ttk.Scrollbar(self)

        self.columns_name = ("ID", "First name", "Surname", "Class")
        self.students_treeview = ttk.Treeview(
            self,
            selectmode="extended",
            columns=self.columns_name,
            show="headings"
        )

        # Manage widgets (positioning, interation and data)
        self.create_headings_for_students_treeview()
        self.position_widgets()
        self.connect_treeview_with_scrollbar()
        self.set_initial_values()

    def position_widgets(self):
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.students_treeview.pack(expand=True, fill=tk.BOTH)

    def connect_treeview_with_scrollbar(self):
        self.students_treeview.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.students_treeview.yview)

    def create_headings_for_students_treeview(self):
        for column in self.columns_name:
            self.students_treeview.heading(column, text=column, anchor=tk.CENTER)

    @staticmethod
    def fetch_students(sorting_element: str, sorting_order: str, class_name: str, surname="") -> (list[(str, str)], str):
        return fetching_students_from_db.get_students(sorting_element, sorting_order, class_name, surname)

    def delete_items(self):
        for child in self.students_treeview.get_children():
            self.students_treeview.delete(child)

    def fill_students_treeview(self, values):
        self.delete_items()
        for students_id, first_name, surname, class_name in values:
            self.students_treeview.insert("", tk.END, values=(students_id, first_name, surname, class_name))

    def set_initial_values(self):
        values, info = fetching_students_from_db.get_students("surname", "A-Z", "-None-")

        if info == "Available students":
            self.fill_students_treeview(values)

        self.config(text=info)
