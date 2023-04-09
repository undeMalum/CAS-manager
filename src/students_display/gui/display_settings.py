import tkinter as tk
from tkinter import ttk

from src.students_display.db import fetching_classes_from_db

PAD_X = 10
PAD_Y = 10


class DisplaySettingsLabelFrame(ttk.LabelFrame):
    def __init__(self, root):
        super().__init__(root, text="Display settings")

        # user can choose by which data (surname or first name)
        # students will be sorted
        self.sorting_element_label = ttk.Label(self, text="Order by:")
        self.sorting_elements = ["surname", "first_name"]
        self.sorting_element_combobox = ttk.Combobox(
            self,
            state="readonly",
            values=self.sorting_elements
        )
        self.sorting_element_combobox.current(0)  # Default: 'surname'

        # user can choose in which order (asc or desc)
        # students will be sorted
        self.sorting_condition_label = ttk.Label(self, text="Alphabetical:")
        self.sorting_conditions = ["A-Z", "Z-A"]  # asc and desc order respectively
        self.sorting_condition_combobox = ttk.Combobox(
            self,
            state="readonly",
            values=self.sorting_conditions
        )
        self.sorting_condition_combobox.current(0)  # Default: 'A-Z'

        # user can choose from which class
        # students will be displayed
        self.class_name_label = ttk.Label(self, text="Class:")
        self.class_name_combobox = ttk.Combobox(
            self,
            state="readonly",
        )
        self.provide_values_for_class_names_combobox()

        # manage widgets
        self.position_widgets()

        # set responsiveness
        for idx in range(5):
            self.columnconfigure(idx, weight=1)
        self.rowconfigure(0, weight=1)

    def position_widgets(self):
        # Sorting element
        self.sorting_element_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.E)
        self.sorting_element_combobox.grid(column=1, row=0, sticky=tk.EW)

        # Sorting condition
        self.sorting_condition_label.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.E)
        self.sorting_condition_combobox.grid(column=3, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)

        # Class names
        self.class_name_label.grid(column=4, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.E)
        self.class_name_combobox.grid(column=5, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)

    def provide_values_for_class_names_combobox(self):
        values = fetching_classes_from_db.get_class_names()
        self.class_name_combobox.config(values=values)
        self.class_name_combobox.current(0)
