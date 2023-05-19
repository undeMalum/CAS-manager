import tkinter as tk
from tkinter import ttk, messagebox

from src.students_alter.db import inserting_updating_interacting_with_db as db_interaction
from src.students_alter import add_modes


class UpdateDBButton(ttk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, text="Confirm", *args, **kwargs)

    @staticmethod
    def erase(widgets: list) -> None:
        """Remove text from widgets"""
        [widget.delete(0, tk.END) for widget in widgets]

    def choose_mode_add(self, mode: add_modes.AddMode, class_combobox: ttk.Combobox,
                        class_name_entry: ttk.Entry, student_display: ttk.Treeview,
                        first_name_entry: ttk.Entry, surname_entry: ttk.Entry,
                        url_entry: ttk.Entry) -> str:
        """Works as an API between GUI and database"""

        selected_student = student_display.selection()
        if not selected_student and mode not in (1, 2, 4):  # altering classes doesn't require student_display
            return tk.messagebox.showerror("Error", "Choose a student!")
        elif len(selected_student) > 1:
            return tk.messagebox.showerror("Error", "Choose only one student!")

        # interact with datab ase
        try:
            map_mode_to_object = db_interaction.create_mode_to_object_dict(
                class_combobox.get(),
                class_name_entry.get(),
                student_display.item(selected_student[0])["values"][0],
                first_name_entry.get(),
                surname_entry.get(),
                url_entry.get()
            )
        except IndexError:  # when altering the class, we don't need student_display
            map_mode_to_object = db_interaction.create_mode_to_object_dict(
                class_combobox.get(),
                class_name_entry.get(),
                0,
                first_name_entry.get(),
                surname_entry.get(),
                url_entry.get()
            )

        info, description = db_interaction.manage_interaction_with_db(
            mode,
            map_mode_to_object
        )
        if info == "Error":
            return tk.messagebox.showerror(info, description)

        # data from entries must be erased
        self.erase([class_name_entry, first_name_entry, surname_entry, url_entry])
        return tk.messagebox.showinfo(info, description)
