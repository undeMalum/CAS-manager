import implementing_alter_abc as imp
import cas_managing_db

from tkinter import ttk, messagebox, END
import tkinter as tk
from typing import Union
from enum import Enum, auto
import requests


def erase(widgets: list) -> None:
    """Remove text from widgets"""
    [widget.delete(0, END) for widget in widgets]


class AddMode(Enum):
    """Holds modes of the Adding Frame"""
    UPDATE_CLASS = auto()
    NEW_CLASS = auto()
    NEW_STUDENT = auto()


def alter_db(object_to_alter_db: Union[imp.NewStudent, imp.NewClass, imp.UpdateClass]) -> None:
    """Alter db with created object (depending on chosen mode)"""
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


def manage_interaction_with_db(mode: AddMode, chosen_class: tuple[str],
                               class_name: str, first_name: str,
                               surname: str, url: str) -> (str, str):
    """Handles interaction with database. It creates an objects and then alters db with it.
    ---> Problem is to separate creation from use"""
    object_altering_db = object()
    if mode == AddMode.UPDATE_CLASS:
        try:
            object_altering_db = imp.UpdateClass(chosen_class, class_name)
            object_altering_db.exists_in_db(class_name)
        except ValueError as exc:
            return "Error", str(exc)
    if mode == AddMode.NEW_CLASS:
        try:
            object_altering_db = imp.NewClass(class_name)
            object_altering_db.exists_in_db(class_name)
        except ValueError as exc:
            return "Error", str(exc)
    if mode == AddMode.NEW_STUDENT:
        try:
            object_altering_db = imp.NewStudent(first_name, surname, url, chosen_class)
        except (ValueError, requests.exceptions.RequestException) as exc:
            return "Error", str(exc)
    alter_db(object_altering_db)
    return "Completed!", "Operation completed successfully!"


def choose_mode_add(mode: AddMode, class_listbox: tk.Listbox,
                    class_name_entry: ttk.Entry, first_name_entry: ttk.Entry,
                    surname_entry: ttk.Entry, url_entry: ttk.Entry) -> str:
    """Works as an API between GUI and database"""
    # interact with database
    info, description = manage_interaction_with_db(
        mode,
        class_listbox.get(class_listbox.curselection()),
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
