import tkinter as tk
from tkinter import ttk

from src.students_alter.gui import modes_frames


class AddFrame(ttk.LabelFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.modes_notebook = modes_frames.ModesNotebook(self)

