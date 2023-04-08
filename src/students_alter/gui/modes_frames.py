import tkinter as tk
from tkinter import ttk

from src.students_alter import add_modes

PAD_X = 10
PAD_Y = 10


class RadiobuttonLabelFrame(ttk.LabelFrame):
    """Frame that hold all radiobuttons (modes) together"""
    def __init__(self, root):
        super().__init__(root)
        self["text"] = "Choose mode"

        # Variable for communicating radiobuttons (modes)
        self.mode = tk.IntVar(
            self,
            add_modes.AddMode.NEW_STUDENT
        )

        # Define raddiobuttons (modes) insides the frame
        self.add_student_radiobutton = ttk.Radiobutton(
            self,
            text="Add student",
            value=add_modes.AddMode.NEW_STUDENT,
            variable=self.mode
        )
        self.update_student_radiobutton = ttk.Radiobutton(
            self,
            text="Update student",
            value=add_modes.AddMode.UPDATE_STUDENT,
            variable=self.mode
        )
        self.add_class_radiobutton = ttk.Radiobutton(
            self,
            text="Add class",
            value=add_modes.AddMode.NEW_CLASS,
            variable=self.mode
        )
        self.update_class_radiobutton = ttk.Radiobutton(
            self,
            text="Update class",
            value=add_modes.AddMode.UPDATE_CLASS,
            variable=self.mode
        )

        # Place radiobuttons insides the radiobutton_label_frame
        self.position_radiobuttons()

        # set responsiveness
        for idx in range(4):
            self.columnconfigure(idx, weight=1)
        self.rowconfigure(0, weight=1)

    def position_radiobuttons(self):
        """Place radiobuttons insides the radiobutton_label_frame"""
        self.add_student_radiobutton.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
        self.update_student_radiobutton.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y)
        self.add_class_radiobutton.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y)
        self.update_class_radiobutton.grid(column=3, row=0, padx=PAD_X, pady=PAD_Y)
