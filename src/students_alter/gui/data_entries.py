import tkinter as tk
from tkinter import ttk

PAD_X = 10
PAD_Y = 10


class StudentEntriesFrame(tk.Frame):
    """Manages frame for creating/updating a student record"""
    def __init__(self, root):
        super().__init__(root)

        # define entries with descriptions
        self.first_name_label = ttk.Label(self, text="First name:")
        self.first_name_entry = ttk.Entry(self)

        self.surname_label = ttk.Label(self, text="Surname:")
        self.surname_entry = ttk.Entry(self)

        self.url_label = ttk.Label(self, text="URL:")
        self.url_entry = ttk.Entry(self)

        # position widgets
        self.position_entries_and_labels()

        # set responsiveness
        for idx in range(4):
            self.columnconfigure(idx, weight=1)
        for idx in range(2):
            self.rowconfigure(idx, weight=1)

    def position_entries_and_labels(self):
        self.first_name_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
        self.first_name_entry.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y)

        self.surname_label.grid(column=2, row=0, padx=PAD_X, pady=PAD_Y)
        self.surname_entry.grid(column=3, row=0, padx=PAD_X, pady=PAD_Y)

        self.url_label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y)
        self.url_entry.grid(column=1, row=1, columnspan=3, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)


class ClassEntriesFrame(tk.Frame):
    """Manages frame for creating/updating a class record"""
    def __init__(self, root):
        super().__init__(root)

        self.class_name_label = ttk.Label(self, text="Class name:")
        self.class_name_entry = ttk.Entry(self)

        # position widgets
        self.position_entries_and_labels()

        # set responsiveness
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

    def position_entries_and_labels(self):
        self.class_name_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.W)
        self.class_name_entry.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.E)


class DataEntriesFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, highlightbackground="#595959", highlightthickness=1)

        self.students_frame = StudentEntriesFrame(self)
        self.classes_frame = ClassEntriesFrame(self)

        self.frames = dict()
        self.fill_frames_variable()
        self.change_frame(self.students_frame.__class__.__name__)  # by default students frame is set

        # set responsiveness
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def fill_frames_variable(self):
        for frame in (self.students_frame, self.classes_frame):
            frame_name = frame.__class__.__name__
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
            # frame.grid_columnconfigure(0, weight=1)

    def change_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
