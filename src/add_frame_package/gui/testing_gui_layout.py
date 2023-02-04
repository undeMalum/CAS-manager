import tkinter as tk
from tkinter import ttk

from add_frame_layout import AddFrame

root = tk.Tk()
root.geometry("500x200")
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "../../../Forest-ttk-theme/forest-dark.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-dark")
add_frame = AddFrame(root)
add_frame.pack()

root.mainloop()
