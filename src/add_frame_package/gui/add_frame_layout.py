import tkinter as tk
from tkinter import ttk

from src.add_frame_package.gui import modes_frames, data_entries


class AddFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Create frame for radiobuttons (modes)
        self.modes_frame = modes_frames.RadiobuttonLabelFrame(self)

        # Create frame for entries (data for db alteration)
        self.data_entries_frame = data_entries.DataEntriesFrame(self)

        # Use radiobuttons to switch between frames
        self.give_modes_frame_radiobuttons_commands()

        # Position frames
        self.position_frames()

    def position_frames(self):
        self.modes_frame.grid(column=0, row=0)
        self.data_entries_frame.grid(column=0, row=1)

    def give_modes_frame_radiobuttons_commands(self):
        # Obtain name of each frame for switching
        students_frame_name = self.data_entries_frame.students_frame.__class__.__name__
        classes_frame_name = self.data_entries_frame.classes_frame.__class__.__name__

        self.modes_frame.add_student_radiobutton.config(
            command=lambda: self.data_entries_frame.change_frame(students_frame_name)
        )
        self.modes_frame.update_student_radiobutton.config(
            command=lambda: self.data_entries_frame.change_frame(students_frame_name)
        )
        self.modes_frame.add_class_radiobutton.config(
            command=lambda: self.data_entries_frame.change_frame(classes_frame_name)
        )
        self.modes_frame.update_class_radiobutton.config(
            command=lambda: self.data_entries_frame.change_frame(classes_frame_name)
        )
