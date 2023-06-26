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
        self.update_class = ttk.Frame(self)
        self.add_student = ttk.Frame(self)
        self.update_student = ttk.Frame(self)

        # Give weight to Tabs
        self.give_weight()

        # Give functionalities to Tabs
        self.students_entries_add = data_entries.StudentEntriesFrame(self.add_student)
        self.students_entries_update = data_entries.StudentEntriesFrame(self.update_student)

        self.students_entries_add = data_entries.StudentEntriesFrame(self.add_student)
        self.students_entries_update = data_entries.StudentEntriesFrame(self.update_student)

    def give_weight(self):
        self.add_class.columnconfigure(index=0, weight=1)
        self.add_class.rowconfigure(index=0, weight=1)

        self.update_class.columnconfigure(index=0, weight=1)
        self.update_class.rowconfigure(index=0, weight=1)

        self.add_student.columnconfigure(index=0, weight=1)
        self.update_student.rowconfigure(index=0, weight=1)


# class RadiobuttonLabelFrame(ttk.LabelFrame):
#     """Frame that hold all radiobuttons (modes) together"""
#     def __init__(self, root):
#         super().__init__(root)
#         self["text"] = "Choose mode"
#
#         # Variable for communicating radiobuttons (modes)
#         self.mode = tk.IntVar(
#             self,
#             add_modes.AddMode.NEW_STUDENT.value
#         )
#
#         # Define raddiobuttons (modes) insides the frame
#         self.add_student_radiobutton = ttk.Radiobutton(
#             self,
#             text="Add student",
#             value=add_modes.AddMode.NEW_STUDENT.value,
#             variable=self.mode
#         )
#         self.update_student_radiobutton = ttk.Radiobutton(
#             self,
#             text="Update student",
#             value=add_modes.AddMode.UPDATE_STUDENT.value,
#             variable=self.mode
#         )
#         self.add_class_radiobutton = ttk.Radiobutton(
#             self,
#             text="Add class",
#             value=add_modes.AddMode.NEW_CLASS.value,
#             variable=self.mode
#         )
#         self.update_class_radiobutton = ttk.Radiobutton(
#             self,
#             text="Update class",
#             value=add_modes.AddMode.UPDATE_CLASS.value,
#             variable=self.mode
#         )
#
#         # Place radiobuttons insides the radiobutton_label_frame
#         self.position_radiobuttons()
#
#         # set responsiveness
#         for idx in range(8):
#             self.columnconfigure(idx, weight=1)
#         self.rowconfigure(0, weight=1)
#
#     def position_radiobuttons(self):
#         """Place radiobuttons insides the radiobutton_label_frame"""
#         self.add_student_radiobutton.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
#         self.update_student_radiobutton.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y)
#         self.add_class_radiobutton.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y)
#         self.update_class_radiobutton.grid(column=3, row=0, padx=PAD_X, pady=PAD_Y)
