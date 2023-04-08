import tkinter as tk
from tkinter import ttk

from src.students_display.gui.students_view import StudentsView
from src.paths.theme_path import THEME_DARK

root = tk.Tk()
root.geometry("500x200")
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", THEME_DARK)

# Set the theme with the theme_use method
style.theme_use("forest-dark")
add_frame = StudentsView(root)
add_frame.pack()

root.mainloop()
