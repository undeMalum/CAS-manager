import tkinter as tk
from tkinter import ttk

from src.students_alter.gui import modes_frames


class AddFrame(ttk.LabelFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, text="Choose mode", *args, **kwargs)

        self.modes_notebook = modes_frames.ModesNotebook(self)
        self.modes_notebook.grid(row=0, column=0)
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)


if __name__ == "__main__":
    from src.paths.theme_path import THEME_DARK

    r = tk.Tk()
    r.geometry("500x200")
    # Create a style
    style = ttk.Style(r)

    # Import the tcl file
    r.tk.call("source", THEME_DARK)

    # Set the Forest-ttk-theme with the theme_use method
    style.theme_use("forest-dark")
    add_frame = AddFrame(r)
    add_frame.pack()

    r.mainloop()
