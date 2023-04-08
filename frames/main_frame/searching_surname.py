from tkinter import Entry, END


class EntrySurname(Entry):
    """This widget allows the user to retrieve students with given surname."""

    def reset_searching_surname(self):
        self.delete(0, END)
        self.insert(0, "Enter surname")

    def initial_settings(self, text):
        self.insert(0, text)
        self.bind("<FocusIn>", lambda e: self.delete(0, END))
        self.bind("<FocusOut>", lambda e: self.reset_searching_surname())
