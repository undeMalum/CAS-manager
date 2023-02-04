import tkinter as tk
from tkinter import ttk, messagebox

from src.add_frame_package.db import inserting_updating_interacting_with_db as db_interaction
from src.add_frame_package import add_modes


def erase(widgets: list) -> None:
    """Remove text from widgets"""
    [widget.delete(0, tk.END) for widget in widgets]


def choose_mode_add(mode: add_modes.AddMode, class_combobox: ttk.Combobox,
                    class_name_entry: ttk.Entry, student_display: ttk.Treeview,
                    first_name_entry: ttk.Entry, surname_entry: ttk.Entry,
                    url_entry: ttk.Entry) -> str:
    """Works as an API between GUI and database"""
    # interact with database
    map_mode_to_object = db_interaction.create_mode_to_object_dict(
        class_combobox.get(),
        class_name_entry.get(),
        student_display.item(student_display.selection())["values"][0],
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
    erase([class_name_entry, first_name_entry, surname_entry, url_entry])
    return tk.messagebox.showinfo(info, description)
