import tkinter as tk
from tkinter import ttk

from src.students_alter.gui import data_entries, excel_handler

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
        self.handle_excel = ttk.Frame(self)
        self.add(self.handle_excel, text="Add multiple students")

        # Give weight to Tabs
        self.give_weight()

        # Give functionalities to Tabs
        self.class_entries_add = data_entries.ClassEntriesFrame(self.add_class)
        self.class_entries_add.grid(row=0, column=0, sticky=tk.NSEW)
        self.class_entries_update = data_entries.ClassEntriesFrame(self.update_class)
        self.class_entries_update.grid(row=0, column=0, sticky=tk.NSEW)

        self.students_entries_add = data_entries.StudentEntriesFrame(self.add_student)
        self.students_entries_add.grid(row=0, column=0, sticky=tk.NSEW)
        self.students_entries_update = data_entries.StudentEntriesFrame(self.update_student)
        self.students_entries_update.grid(row=0, column=0, sticky=tk.NSEW)

        self.handle_excel_tab = excel_handler.ExcelHandler(self.handle_excel)
        self.handle_excel_tab.grid(row=0, column=0, sticky=tk.NSEW)

    def give_weight(self):
        self.add_class.columnconfigure(index=0, weight=1)
        self.add_class.rowconfigure(index=0, weight=1)

        self.update_class.columnconfigure(index=0, weight=1)
        self.update_class.rowconfigure(index=0, weight=1)

        self.add_student.columnconfigure(index=0, weight=1)
        self.add_student.rowconfigure(index=0, weight=1)

        self.update_student.columnconfigure(index=0, weight=1)
        self.update_student.rowconfigure(index=0, weight=1)

        self.handle_excel.columnconfigure(index=0, weight=1)
        self.handle_excel.rowconfigure(index=0, weight=1)

    def return_current_tab(self):
        return self.index(self.select())


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
    notebook = ModesNotebook(root)
    notebook.pack()

    root.mainloop()
