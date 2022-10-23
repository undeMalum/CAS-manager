import implementating_alter_abc
import the_base_for_inserting_updating_db as abc_altering_db
from tkinter import ttk, messagebox, END
from typing import Type
import tkinter as tk
from enum import Enum, auto


class Employee(Enum):
    CEO = auto()
    SECRETARY = auto()
    INTERN = auto()


def show_info(widget, pop_up_text: str, static_text: str) -> None:
    widget.config(text=pop_up_text)
    widget.after(3000, lambda: widget.config(text=static_text))


def erase(widgets: list) -> None:
    [widget.delete(0, END) for widget in widgets]


def add_student(info_label: ttk.Label, add_listbox: tk.Listbox, first_name: str, surname: str, url: str) -> str:
    # get all indices from the chosen range
    class_name_idxs = add_listbox.curselection()

    # create student instance
    student = implementating_alter_abc.NewStudent(first_name, surname, url, class_name_idxs)

    # make sure all parameters are given
    if not student.data_is_correct:
        return tk.messagebox.showerror("Error", "You didn't provide all data or provided data was incorrect.")

    student = add_listbox.get(class_name_idxs[0])
    insert_student(first_name, surname, class_name_values[0], url)
    # displaying information about adding student (temporarily)
    show_info(info_label, "Added successfully!", "(Updated/added class name)")

    # erasing entry boxes so the user doesn't have to do it by himself
    erase([name_entry, surname_entry, url_entry])


def class_chosen(class_listbox: tk.Listbox) -> bool:
    if not class_listbox.curselection():
        return False
    return True


def parameters_given(object_to_check: Type[abc_altering_db.AlterDB]) -> bool:
    if not object_to_check.data_is_correct:
        return False
    return True


def alter_db(object_to_alter_db: Type[abc_altering_db.AlterDB]) -> None:
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


alter_db(implementating_alter_abc.NewStudent)
