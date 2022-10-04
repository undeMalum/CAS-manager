from tkinter import Button, Frame, CENTER, Listbox, END

from .cas_managing_db_two import fetch_classes


def change_frame(previous_frame: Frame, next_frame: Frame):
    # make previous frame disappear
    previous_frame.pack_forget()
    previous_frame.place_forget()

    # change to next frame
    next_frame.pack()
    next_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def update_classes(classes_listbox: Listbox, students_listbox: Listbox = None):
    # refresh listbox displaying classes as some changes may occur
    fetch_classes(classes_listbox)

    # enable searching_name to reset
    classes_listbox.focus_set()

    # add_frame has no listbox displaying students
    if students_listbox is None:
        return

    # reset students
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
