import tkinter as tk
from tkinter import ttk

from src.students_display.gui.display_settings import DisplaySettingsLabelFrame
from src.paths.theme_path import THEME_DARK

root = tk.Tk()
root.geometry("500x200")
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", THEME_DARK)

# Set the Forest-ttk-theme with the theme_use method
style.theme_use("forest-dark")
add_frame = DisplaySettingsLabelFrame(root)
add_frame.pack()

root.mainloop()
