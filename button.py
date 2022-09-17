from tkinter import Frame, Listbox, CENTER, END, DISABLED
from cas_managing_db import fetch_classes


# refresh listbox displaying classes as some changes may have occurred
def fill_with_classes(classes_listbox: 'Listbox', students_listbox: 'Listbox') -> None:
    fetch_classes(classes_listbox)
    # add_frame has no listbox displaying students, therefore students_listbox is set to temp listbox
    # making no changes
    if classes_listbox != classes_display_add:
        students_listbox.delete(0, END)
        students_listbox.insert(END, "Choose class")
    else:
        # enable searching_name to reset
        classes_listbox.focus_set()
        if add_mode.get() == 3:  # if new class mode was chosen, listbox displaying classes must stay disabled
            classes_listbox.config(state=DISABLED)


# hide current frame and make next visible
def change_frame(previous_frame: 'Frame', next_frame: 'Frame') -> None:
    previous_frame.pack_forget()
    previous_frame.place_forget()
    next_frame.pack()
    next_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
