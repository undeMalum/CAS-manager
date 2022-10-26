import implementing_alter_abc as imp

from tkinter import ttk, messagebox, END
import tkinter as tk
from typing import Union, Callable
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


class AddMode(Enum):
    UPDATE_CLASS = auto()
    NEW_CLASS = auto()
    NEW_STUDENT = auto()


def alter_db(object_to_alter_db: Union[imp.NewStudent, imp.NewClass, imp.UpdateClass]) -> None:
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


def class_given(class_listbox: tk.Listbox) -> str:
    if not class_listbox.curselection():
        return tk.messagebox.showerror("Error", "No class given!")


def create_update_class(old_class_name: tuple[str], new_class_name: str) -> imp.UpdateClass:
    return imp.UpdateClass(old_class_name, new_class_name)


def create_insert_class(class_name: str) -> imp.NewClass:
    return imp.NewClass(class_name)


def create_insert_student(first_name: str, surname: str,
                          url: str, class_name: tuple[str]) -> imp.NewStudent:
    return imp.NewStudent(first_name, surname, url, class_name)


def db_alteration(object_altering_db: Union[imp.UpdateClass, imp.NewClass, imp.NewStudent], alter_class: bool):
    if not object_altering_db.data_is_correct:
        return tk.messagebox.showerror("Error", "Provided data is incorrect!")

    if alter_class:
        if object_altering_db.exists_in_db:
            return tk.messagebox.showerror("Error", "Class of given name already exists!")

    # inserting class into db
    alter_db(object_altering_db)

    return tk.messagebox.showinfo("Completed!", "Operation completed successfully!")


def choose_mode_add(mode: AddMode, class_listbox: tk.Listbox,
                    class_name_entry: ttk.Entry, first_name_entry: ttk.Entry,
                    surname_entry: ttk.Entry, url_entry: ttk.Entry) -> None:

    alter_class = False
    # make sure class was chosen in listbox
    if mode == AddMode.UPDATE_CLASS or mode == AddMode.NEW_CLASS:
        alter_class = True
        class_given(class_listbox)

    map_mode_to_class: dict[AddMode: Callable] = {
        AddMode.UPDATE_CLASS: create_update_class(
            class_listbox.get(class_listbox.curselection()),
            class_name_entry.get()
        ),
        AddMode.NEW_CLASS: create_insert_class(
            class_name_entry.get()
        ),
        AddMode.NEW_STUDENT: create_insert_student(
            first_name_entry.get(),
            surname_entry.get(),
            url_entry.get(),
            class_listbox.get(class_listbox.curselection())
        )
    }

    object_altering_db = map_mode_to_class[mode]

    db_alteration(object_altering_db, alter_class)

    erase([class_listbox, class_name_entry, first_name_entry, surname_entry, url_entry])
    # erasing values from widgets: change state if needed, come back to the previous state,
    # update class_listbox after altering classes
