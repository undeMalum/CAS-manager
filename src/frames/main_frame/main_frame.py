from tkinter import Frame, Listbox, Scrollbar, Button, CENTER, NSEW, END, Tk

from .searching_surname import EntrySurname
from ..cas_managing_db_two import fetch_classes
from .go_to_url import go_url


class AvailableClasses:
    def __int__(self, root: Tk, f: int):
        self.main = root
        self.f = f
        # for displaying and searching through available classes
        self.temp_classes = Listbox(self.main)  # listbox used only to make a margin; it won't be considered

        self.scrollbar_classes = Scrollbar(
            self.temp_classes,
            width=12
        )

        self.classes = Listbox(
            self.temp_classes,
            selectmode="single",
            yscrollcommand=self.scrollbar_classes.set,
            font=self.f,
            width=12,
            height=11,
            highlightthickness=0,
            borderwidth=0
        )

        self.scrollbar_classes.config(command=self.classes.yview)
        # initial fulfillment of classes listbox
        fetch_classes(self.classes)


class MainFrame:
    """This is main frame where the user can retrieve stored urls (in this case links to student's portfolios)"""

    def __int__(self, root: Tk, chosen_class: str, f: int) -> None:
        self.chosen_class = chosen_class
        self.f = f

        # creating widgets inside the main frame
        self.main = Frame(
            root,
            height=650,
            width=450
        )

        # for displaying and searching through available classes
        self.temp_classes = Listbox(self.main)  # listbox used only to make a margin; it won't be considered

        self.scrollbar_classes = Scrollbar(
            self.temp_classes,
            width=12
        )

        self.classes = Listbox(
            self.temp_classes,
            selectmode="single",
            yscrollcommand=self.scrollbar_classes.set,
            font=self.f,
            width=12,
            height=11,
            highlightthickness=0,
            borderwidth=0
        )

        self.scrollbar_classes.config(command=self.classes.yview)
        # initial fulfillment of classes listbox
        fetch_classes(self.classes)

        # for confirming choice of class
        self.class_chosen_url = Button(
            self.main,
            text="Accept",
            command=lambda: accept_class(
                self.students,
                self.classes
            )
        )

        # for searching students based on their surname within given class
        self.searching_surname = EntrySurname(self.main)
        self.searching_surname.initial_settings("Enter surname")
        self.confirm_surname = Button(
            self.main,
            text="Search",
            command=lambda: search_for_student(
                self.students,
                self.searching_surname.get(),
                self.chosen_class
            )
        )

        # for displaying available students within the given class
        self.scrollbar_students = Scrollbar(self.main)
        self.students = Listbox(
            self.main,
            selectmode="single",
            yscrollcommand=self.scrollbar_students.set,
            height=10,
            font=self.f
        )
        self.scrollbar_students.config(command=self.students.yview)
        # warning that reminds user of choosing class
        self.students.insert(END, "Choose class")
        # for redirecting users into the chosen student's portfolio
        self.go_to_url = Button(self.main, text="Go", command=lambda: go_url(self.students, self.chosen_class))

        # going to other functionalities of the program, ie adding/updating and removing elements
        self.go_to_add_main = Button(self.main, text="Add/Update", height=3, command=lambda: move(self.main, add_frame,
                                                                                             classes_display_add,
                                                                                             temp_classes_add))
        self.go_to_remove_main = Button(self.main, text="Remove", height=3, command=lambda: move(self.main, remove_frame,
                                                                                            classes_display_rem,
                                                                                            students_display_rem))

    def place_widgets_main(self):
        self.main.pack()
        self.main.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.temp_classes.grid(column=1, row=0, rowspan=2, sticky=NSEW)
        # scrollbar_classes and classes are placed inside temp_classes
        self.scrollbar_classes.grid(column=0, row=0, rowspan=2, sticky=NSEW)
        self.classes.grid(column=1, row=0, padx=5, sticky=NSEW)

        self.class_chosen_url.grid(column=2, row=0, rowspan=2, sticky=NSEW)

        self.searching_surname.grid(column=4, row=0, sticky=NSEW)
        self.confirm_surname.grid(column=5, row=0, sticky=NSEW)

        self.scrollbar_students.grid(column=3, row=1, sticky=NSEW)
        self.students.grid(column=4, row=1, columnspan=2, sticky=NSEW)
        self.go_to_url.grid(column=6, row=0, rowspan=2, sticky=NSEW)

        self.go_to_add_main.grid(column=0, row=3, columnspan=4, sticky=NSEW)
        self.go_to_remove_main.grid(column=4, row=3, columnspan=3, sticky=NSEW)
