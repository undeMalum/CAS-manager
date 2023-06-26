import tkinter as tk
from tkinter import ttk

from src.students_alter.gui import data_entries

PAD_X = 10
PAD_Y = 10


class ModesNotebook(ttk.Notebook):
    """Notebook that changes the mode of db alteration"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define Tabs inside the ModesNotebook
        self.add_class = ttk.Frame(self)
        self.add(self.add_class, text="Add class")
        self.update_class = ttk.Frame(self)
        self.add(self.update_class, text="Update class")
        self.add_student = ttk.Frame(self)
        self.add(self.add_student, text="Add student")
        self.update_student = ttk.Frame(self)
        self.add(self.update_student, text="Update student")

        # Give weight to Tabs
        self.give_weight()

        # Give functionalities to Tabs
        self.class_entries_add = data_entries.ClassEntriesFrame(self.add_class)
        self.class_entries_add.grid(row=0, column=0)
        self.class_entries_update = data_entries.ClassEntriesFrame(self.update_class)
        self.class_entries_update.grid(row=0, column=0)

        self.students_entries_add = data_entries.StudentEntriesFrame(self.add_student)
        self.students_entries_add.grid(row=0, column=0)
        self.students_entries_update = data_entries.StudentEntriesFrame(self.update_student)
        self.students_entries_update.grid(row=0, column=0)

    def give_weight(self):
        self.add_class.columnconfigure(index=0, weight=1)
        self.add_class.rowconfigure(index=0, weight=1)

        self.update_class.columnconfigure(index=0, weight=1)
        self.update_class.rowconfigure(index=0, weight=1)

        self.add_student.columnconfigure(index=0, weight=1)
        self.update_student.rowconfigure(index=0, weight=1)


if __name__ == "__main__":
    from src.paths.theme_path import THEME_DARK

    root = tk.Tk()
    root.geometry("500x200")
    # Create a style
    style = ttk.Style(root)

    # Import the tcl file
    root.tk.call("source", THEME_DARK)

    # Set the Forest-ttk-theme with the theme_use method
    style.theme_use("forest-dark")
    add_frame = ModesNotebook(root)
    add_frame.pack()

    root.mainloop()