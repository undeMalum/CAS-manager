import inserting_updating_interacting_with_db
from add_modes import AddMode
import cas_managing_db

from tkinter import ttk, messagebox, END
import tkinter as tk


def erase(widgets: list) -> None:
    """Remove text from widgets"""
    [widget.delete(0, END) for widget in widgets]


def choose_mode_add(mode: AddMode, class_listbox: tk.Listbox,
                    class_name_entry: ttk.Entry, first_name_entry: ttk.Entry,
                    surname_entry: ttk.Entry, url_entry: ttk.Entry) -> str:
    """Works as an API between GUI and database"""
    # interact with database
    info, description = inserting_updating_interacting_with_db.manage_interaction_with_db(
        mode,
        class_listbox.get(class_listbox.curselection())[0],
        class_name_entry.get(),
        first_name_entry.get(),
        surname_entry.get(),
        url_entry.get()
    )
    if info == "Error":
        return tk.messagebox.showerror(info, description)

    # if the state of class_listbox is disabled, we must change it to provide new data
    cas_managing_db.fetch_classes(class_listbox)

    # data from entries must be erased
    erase([class_name_entry, first_name_entry, surname_entry, url_entry])
    return tk.messagebox.showinfo(info, description)
