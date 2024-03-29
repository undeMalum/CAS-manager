import tkinter as tk
from tkinter import ttk

from src.students_display.db import (
    removing_from_db
)

PAD_X = 5
PAD_Y = 10


class ToolsLabelFrame(ttk.LabelFrame):
    def __init__(self, root):
        super().__init__(root, text="Tools")

        # Search tool (by surname)
        self.search_label = ttk.Label(self, text="Search student(s):")
        self.search_entry = ttk.Entry(self)
        self.set_defaults_for_search_entry("Enter surname")

        self.store_entry_content = ""
        self.search_button = ttk.Button(self, text="Search")

        # Separate the tools
        self.tool_separator = ttk.Separator(self, orient=tk.VERTICAL)

        # Delete tool
        self.delete_label = ttk.Label(self, text="Delete:")
        self.delete_combobox_values = ["student(s)", "class"]
        self.delete_combobox = ttk.Combobox(
            self,
            state="readonly",
            values=self.delete_combobox_values,
        )
        self.delete_combobox.current(0)

        self.delete_button = ttk.Button(self, text="Confirm")  # Replace with bin emoji if possible

        # Manage widgets
        self.position_widgets()

        # set responsiveness
        for idx in range(7):
            self.columnconfigure(idx, weight=1)
        self.rowconfigure(0, weight=1)

    def position_widgets(self):
        # Search tool
        self.search_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.E)
        self.search_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)
        self.search_button.grid(column=2, row=0, padx=10, pady=10, sticky=tk.E)

        # Separator
        self.tool_separator.grid(column=3, row=0, padx=10, pady=10, sticky=tk.NS)

        # Delete tool
        self.delete_label.grid(column=4, row=0, padx=10, pady=10, sticky=tk.E)
        self.delete_combobox.grid(column=5, row=0, padx=10, pady=10, sticky=tk.EW)
        self.delete_button.grid(column=6, row=0, padx=10, pady=10, sticky=tk.EW)

    def reset_searching_surname(self):
        self.store_entry_content = self.search_entry.get()
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Enter surname")

    def set_defaults_for_search_entry(self, text):
        self.search_entry.insert(0, text)
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, tk.END))
        self.search_entry.bind("<FocusOut>", lambda e: self.reset_searching_surname())

    @staticmethod
    def remove_student(students_id: list[int]):
        removing_from_db.delete_student(students_id)

    @staticmethod
    def remove_class(class_name: str):
        removing_from_db.delete_class(class_name)
