from tkinter import Button, Frame, CENTER, Listbox, DISABLED, END

from .cas_managing_db_two import fetch_classes


def change_frame(previous_frame: Frame, next_frame: Frame):
    previous_frame.pack_forget()
    previous_frame.place_forget()
    next_frame.pack()
    next_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def update_classes(classes_listbox: Listbox, students_listbox: Listbox):
    # refresh listbox displaying classes as some changes may occur
    fetch_classes(classes_listbox)
    # add_frame has no listbox displaying students, therefore students_listbox is set to temp listbox
    # making no changes
    if classes_listbox == classes_display_add:
        # enable searching_name to reset
        classes_listbox.focus_set()
        if add_mode.get() == 3:  # if new class mode was chosen, listbox displaying classes must stay disabled
            classes_listbox.config(state=DISABLED)
        return

    students_listbox.delete(0, END)
    students_listbox.insert(END, "Choose class")


class MoveButton(Button):
    @classmethod
    def move(cls, previous_frame: Frame, next_frame: Frame, classes_listbox: Listbox,
             students_listbox: Listbox) -> None:
        # forget chosen class to avoid situation when user can click "Accept" without choosing class
        cls.store_class_name = ""
        change_frame(previous_frame, next_frame)
        update_classes(classes_listbox, students_listbox)
