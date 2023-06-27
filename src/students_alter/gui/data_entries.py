import tkinter as tk
from tkinter import ttk

from abc import ABC, abstractmethod

PAD_X = 10
PAD_Y = 10


class DataEntries(ABC):
    @abstractmethod
    def return_entries_values(self):
        pass

    @abstractmethod
    def erase(self):
        pass


class StudentEntriesFrame(ttk.Frame, DataEntries):
    """Manages frame for creating/updating a student record"""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # define entries with descriptions
        self.first_name_label = ttk.Label(self, text="First name:")
        self.first_name_entry = ttk.Entry(self)

        self.surname_label = ttk.Label(self, text="Surname:")
        self.surname_entry = ttk.Entry(self)

        self.url_label = ttk.Label(self, text="URL:")
        self.url_entry = ttk.Entry(self)

        # position widgets
        self.position_entries_and_labels()

        # set responsiveness
        for idx in range(4):
            self.columnconfigure(idx, weight=1)
        for idx in range(2):
            self.rowconfigure(idx, weight=1)

    def position_entries_and_labels(self):
        self.first_name_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
        self.first_name_entry.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y)

        self.surname_label.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y)
        self.surname_entry.grid(column=3, row=0, padx=PAD_X, pady=PAD_Y)

        self.url_label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y)
        self.url_entry.grid(column=1, row=1, columnspan=3, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)

    def return_entries_values(self):
        return self.first_name_entry.get(), self.surname_entry.get(), self.url_entry.get()

    def erase(self) -> None:
        """Remove text from widgets"""
        self.first_name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)


class ClassEntriesFrame(ttk.Frame, DataEntries):
    """Manages frame for creating/updating a class record"""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.class_name_label = ttk.Label(self, text="Class name:")
        self.class_name_entry = ttk.Entry(self)

        # position widgets
        self.position_entries_and_labels()

        # set responsiveness
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

    def position_entries_and_labels(self):
        self.class_name_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.W)
        self.class_name_entry.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.E)

    def return_entries_values(self):
        return self.class_name_entry.get()

    def erase(self) -> None:
        """Remove text from widgets"""
        self.class_name_entry.delete(0, tk.END)
