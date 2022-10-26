import implementing_alter_abc as imp

from tkinter import ttk, messagebox, END
import tkinter as tk
from typing import Union
from enum import Enum, auto


def show_info(widget, pop_up_text: str, static_text: str) -> None:
    widget.config(text=pop_up_text)
    widget.after(3000, lambda: widget.config(text=static_text))


def erase(widgets: list) -> None:
    [widget.delete(0, END) for widget in widgets]


# def add_student(first_name: str, surname: str, url: str, class_name: tuple[str]) -> str:
#     # create student instance
#     student = imp.NewStudent(first_name, surname, url, class_name_idxs)
#
#     # make sure all parameters are given
#     if not student.data_is_correct:
#         return tk.messagebox.showerror("Error", "You didn't provide all data or provided data was incorrect.")
#
#     student = add_listbox.get(class_name_idxs[0])
#     insert_student(first_name, surname, class_name_values[0], url)
#     # displaying information about adding student (temporarily)
#     show_info(info_label, "Added successfully!", "(Updated/added class name)")
#
#     # erasing entry boxes so the user doesn't have to do it by himself
#     erase([name_entry, surname_entry, url_entry])


def alter_db(object_to_alter_db: Union[imp.NewStudent, imp.NewClass, imp.UpdateClass]) -> None:
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


class AddMode(Enum):
    UPDATE_CLASS = auto()
    NEW_CLASS = auto()
    NEW_STUDENT = auto()


def manage_updating_class_record(old_class_name: tuple[str], new_class_name: str) -> str:
    updated_class = imp.UpdateClass(old_class_name, new_class_name)

    if not updated_class.data_is_correct:
        return tk.messagebox.showerror("Error", "Provided data is incorrect!")

    if updated_class.exists_in_db:
        return tk.messagebox.showerror("Error", "Class of given name already exists!")

    # updating class record
    alter_db(updated_class)

    return tk.messagebox.showinfo("Completed!", "Class updated successfully!")


def manage_inserting_class(class_name: str) -> str:
    inserted_class = imp.NewClass(class_name)

    if not inserted_class.data_is_correct:
        return tk.messagebox.showerror("Error", "Provided data is incorrect!")

    if inserted_class.exists_in_db:
        return tk.messagebox.showerror("Error", "Class of given name already exists!")

    # inserting class into db
    alter_db(inserted_class)

    return tk.messagebox.showinfo("Completed!", "Class added successfully!")


def manage_inserting_student(first_name: str, surname: str,
                             url: str, class_name: tuple[str]) -> str:
    inserted_student = imp.NewStudent(first_name, surname, url, class_name)

    if not inserted_student.data_is_correct:
        return tk.messagebox.showerror("Error", "Provided data is incorrect!")

    # inserting student into db
    alter_db(inserted_student)

    return tk.messagebox.showinfo("Completed!", "Student added successfully!")


def choose_mode_add(mode: AddMode, class_listbox: tk.Listbox,
                    class_name_entry: ttk.Entry, first_name_entry: ttk.Entry,
                    surname_entry: ttk.Entry, url_entry: ttk.Entry) -> str:
    if mode == AddMode.UPDATE_CLASS:
        if not class_listbox.curselection():
            return tk.messagebox.showerror("Error", "No class given!")

        old_class_name = class_listbox.get(class_listbox.curselection())
        new_class_name = class_name_entry.get()
        manage_updating_class_record(old_class_name, new_class_name)
    elif mode == AddMode.NEW_CLASS:
        class_name = class_name_entry.get()
        manage_inserting_class(class_name)
    elif mode == AddMode.NEW_STUDENT:
        if not class_listbox.curselection():
            return tk.messagebox.showerror("Error", "No class given!")

        first_name = first_name_entry.get()
        surname = surname_entry.get()
        url = url_entry.get()
        class_name = class_listbox.get(class_listbox.curselection())

        manage_inserting_student(first_name, surname, url, class_name)

    # erasing values from widgets: change state if needed, come back to the previous state,
    # update class_listbox after altering classes
