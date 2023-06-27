import tkinter as tk
from tkinter import ttk, messagebox

from src.students_alter.db import inserting_updating_interacting_with_db as db_interaction


class UpdateDBButton(ttk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, text="Confirm", *args, **kwargs)

    @staticmethod
    def choose_mode_add(alteration_class, entries_class,
                        need_selected_students: bool, student_display: ttk.Treeview) -> str:
        """Works as an API between GUI and database"""

        # if needed, check if a student was chosen
        if need_selected_students:
            selected_student = student_display.selection()
            if not selected_student:
                return tk.messagebox.showerror("Error", "Choose a student!")
            elif len(selected_student) > 1:
                return tk.messagebox.showerror("Error", "Choose only one student!")

            parameters_to_be_used = (student_display.item(selected_student[0])["values"][0],
                                     *entries_class[0].return_entries_values(), entries_class[1])
        elif entries_class[1] is None:
            parameters_to_be_used = entries_class[0].return_entries_values()
        else:
            parameters_to_be_used = (entries_class[1], *entries_class[0].return_entries_values())

        # call to the db
        info, description = db_interaction.manage_interaction_with_db(
            alteration_class,
            parameters_to_be_used
        )
        if info == "Error":
            return tk.messagebox.showerror(info, description)

        # data from entries must be erased
        entries_class[0].erase()

        return tk.messagebox.showinfo(info, description)
