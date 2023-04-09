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
    go_to_url_button
)
from src.students_alter.gui import add_frame_layout, update_db_button

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
        self.view_tools.delete_button.configure(command=self.remove_from_student_view)
        self.display_settings = display_settings.DisplaySettingsLabelFrame(self)
        self.students_view = students_view.StudentsView(self)
        self.add_frame = add_frame_layout.AddFrame(self)
        self.update_db_button = update_db_button.UpdateDBButton(self, command=self.confirm_update)
        # new widgets
        self.theme = tk.IntVar(self)
        self.theme_switcher = ttk.Checkbutton(
            self,
            style="Switch",
            text="Switch theme",
            variable=self.theme,
            command=self.switch_theme
        )
        self.go_to_url_button = go_to_url_button.URLButton(self, command=self.go_url)

        # give weight
        self.give_weight()

        # display all widgets
        self.position_widgets()

        # make display settings alter the student view section
        self.set_events_for_display_settings()

        # position the window
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{x}+{y}")

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
        if not self.theme.get():
            self.configure(background="#313131")
            self.add_frame.data_entries_frame.students_frame.configure(background="#313131")
            self.add_frame.data_entries_frame.classes_frame.configure(background="#313131")
            self.style.theme_use("forest-dark")
        else:
            self.configure(background="#ffffff")
            self.add_frame.data_entries_frame.students_frame.configure(background="#ffffff")
            self.add_frame.data_entries_frame.classes_frame.configure(background="#ffffff")
            self.style.theme_use("forest-light")

    def alter_students_view(self, surname: str = ""):
        """Function that changes the content of the student view treeview
        as well as the label of the surrounding label frame if required."""
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

    def search_student(self):
        """Function that looks for a student based on the provided surname."""
        surname = self.view_tools.store_entry_content
        if not surname or surname == "Enter surname":
            return tk.messagebox.showerror("Error", "Student surname not provided.")

        self.alter_students_view(surname)

    def confirm_update(self):
        """Function that alters db based on the input from the add frame."""
        self.update_db_button.choose_mode_add(
            self.add_frame.modes_frame.mode.get(),
            self.display_settings.class_name_combobox,
            self.add_frame.data_entries_frame.classes_frame.class_name_entry,
            self.students_view.students_treeview,
            self.add_frame.data_entries_frame.students_frame.first_name_entry,
            self.add_frame.data_entries_frame.students_frame.surname_entry,
            self.add_frame.data_entries_frame.students_frame.url_entry
        )

        self.display_settings.provide_values_for_class_names_combobox()
        self.alter_students_view()

    def set_events_for_display_settings(self):
        self.display_settings.sorting_element_combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: self.alter_students_view()
        )
        self.display_settings.sorting_condition_combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: self.alter_students_view()
        )
        self.display_settings.class_name_combobox.bind(
            "<<ComboboxSelected>>",
            lambda e: self.alter_students_view()
        )

    def remove_from_student_view(self):
        """Function that removes either individual students or entire class of students."""
        if self.view_tools.delete_combobox.get() == "student":
            selected_student = self.students_view.students_treeview.selection()
            if not selected_student:
                return tk.messagebox.showerror("Error", "Choose a student!")
            self.view_tools.remove_student(
                self.students_view.students_treeview.item(
                    selected_student[0]
                )["values"][0]
            )
        else:
            selected_class = self.display_settings.class_name_combobox.get()
            if selected_class == "-None-":
                return tk.messagebox.showerror("Error", "Choose a class!")
            self.view_tools.remove_class(selected_class)
            self.display_settings.provide_values_for_class_names_combobox()

        self.alter_students_view()

    def go_url(self):
        selected_student = self.students_view.students_treeview.selection()
        if not selected_student:
            return tk.messagebox.showerror("Error", "Choose a student!")

        url = self.go_to_url_button.get_url(
            self.students_view.students_treeview.item(
                selected_student[0]
            )["values"][0]
        )

        self.go_to_url_button.open_url(url)


def main():
    main_window = MainWindow()
    main_window.mainloop()


if __name__ == "__main__":
    main()