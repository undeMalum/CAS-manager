import tkinter as tk
from tkinter import ttk, messagebox

from src.paths.theme_path import (
    THEME_DARK,
    THEME_LIGHT
)

from src.students_display.gui import (
    view_tools,
    display_settings,
    students_view,
)
from src.students_alter.gui import add_frame_layout

PAD_X = 10
PAD_Y = 10


class MainWindow(tk.Tk):
    """It joins all GUI elements and provides interaction between them"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set initial parameters for the window
        self.title("CAS manager")
        self.style = ttk.Style(self)  # Create a style
        self.tk.call("source", THEME_DARK)  # Import the tcl file dark
        self.tk.call("source", THEME_LIGHT)  # Import the tcl file light
        self.style.theme_use("forest-dark")  # Set the theme with the theme_use method

        # create widgets
        # pre-prepared widgets
        self.view_tools = view_tools.ToolsLabelFrame(self)
        self.view_tools.search_button.configure(command=self.search_student)
        self.display_settings = display_settings.DisplaySettingsLabelFrame(self)
        self.students_view = students_view.StudentsView(self)
        self.add_frame = add_frame_layout.AddFrame(self)
        # new widgets
        self.theme = tk.IntVar(self)
        self.theme_switcher = ttk.Checkbutton(
            self,
            style="Switch",
            text="Switch theme",
            variable=self.theme,
            command=self.switch_theme
        )
        self.go_to_url_button = ttk.Button(self, text="GO")
        self.update_db_button = ttk.Button(self, text="Confirm")

        # give weight
        self.give_weight()

        # display all widgets
        self.position_widgets()

        # position the window
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")

        # set default theme
        self.switch_theme()

    def give_weight(self):
        self.columnconfigure(index=0, weight=7)
        self.columnconfigure(index=1, weight=3)

        self.rowconfigure(index=0, weight=0)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=5)
        self.rowconfigure(index=4, weight=1)

    def position_widgets(self):
        # pre-prepared widgets
        self.view_tools.grid(column=0, row=1, padx=PAD_X, pady=(0, PAD_Y), sticky=tk.NSEW)

        self.display_settings.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        self.students_view.grid(column=0, row=3, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        self.add_frame.grid(column=1, row=3, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        # new widgets
        self.theme_switcher.grid(column=0, row=4, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        self.go_to_url_button.grid(column=0, row=4, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        self.update_db_button.grid(column=1, row=4, padx=PAD_X, pady=PAD_Y, sticky=tk.NSEW)

        self.theme_switcher.grid(column=0, row=0, padx=PAD_X, sticky=tk.NSEW)

    def switch_theme(self):
        if self.theme.get() == 0:
            self.configure(background="#313131")
            self.add_frame.data_entries_frame.students_frame.configure(background="#313131")
            self.add_frame.data_entries_frame.classes_frame.configure(background="#313131")
            self.style.theme_use("forest-dark")
        else:
            self.configure(background="#ffffff")
            self.add_frame.data_entries_frame.students_frame.configure(background="#ffffff")
            self.add_frame.data_entries_frame.classes_frame.configure(background="#ffffff")
            self.style.theme_use("forest-light")

    def search_student(self):
        surname = self.view_tools.store_entry_content
        if not surname or surname == "Enter surname":
            return tk.messagebox.showerror("Error", "Student surname not provided.")

        students, info = self.students_view.fetch_students(
            self.display_settings.sorting_element_combobox.get(),
            self.display_settings.sorting_condition_combobox.get(),
            self.display_settings.class_name_combobox.get(),
            surname
        )
        if info == "Available students":
            self.students_view.fill_students_treeview(students)
        else:
            self.students_view.delete_items()

        self.students_view.configure(text=info)





if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
