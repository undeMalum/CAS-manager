import tkinter as tk
from tkinter import ttk

from src.add_frame_package import add_modes


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

    def position_radiobuttons(self):
        """Place radiobuttons insides the radiobutton_label_frame"""
        self.add_student_radiobutton.grid(column=0, row=0)
        self.update_student_radiobutton.grid(column=1, row=0)
        self.add_class_radiobutton.grid(column=2, row=0)
        self.update_class_radiobutton.grid(column=3, row=0)
