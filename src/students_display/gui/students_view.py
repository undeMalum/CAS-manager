import tkinter as tk
from tkinter import ttk


class StudentsView(ttk.LabelFrame):
    def __int__(self, root):
        super().__init__(root)

        self.scrollbar = ttk.Scrollbar(self)

        self.columns_name = ("ID", "First name", "Surname", "Class")
        self.students_treeview = ttk.Treeview(
            self,
            selectmode="extended",
            yscrollcommand=self.scrollbar.set,
            columns=self.columns_name
        )
