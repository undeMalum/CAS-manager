from requests import get, exceptions
from tkinter import *
from tkinter import font
from cas_managing_db import *
from tkinter import messagebox
from tkinter import ttk
from src.frames.main_frame.searching_surname import EntrySurname
from src.frames.main_frame.students_based_on_surname import search_for_student
from src.frames.main_frame.go_to_url import go_url


def main():
    # creating window and setting default parameters
    root = Tk()
    root.title("CAS manager")
    root.geometry("650x450")

    # Create a style
    style = ttk.Style(root)

    # Import the tcl file
    root.tk.call("source", "Forest-ttk-theme/forest-dark.tcl")

    # Set the theme with the theme_use method
    style.theme_use("forest-dark")

    # functions for widgets
    # function initialize when switching between frames
    def move(previous_frame: 'Frame', next_frame: 'Frame', classes_listbox: 'Listbox',
             students_listbox: 'Listbox' = None):
        # forget chosen class to avoid situation when user can click "Accept" without choosing class
        global store_class_name
        store_class_name = ""
        # hide previous frame and make new one visible
        previous_frame.pack_forget()
        previous_frame.place_forget()
        next_frame.pack()
        next_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # refresh listbox displaying classes as some changes may occur
        fetch_classes(classes_listbox)

        # enable searching_name to reset
        classes_listbox.focus_set()

        if students_listbox is None:
            return

        # reset students
        students_listbox.delete(0, END)
        students_listbox.insert(END, "Choose class")

    def erase(widgets: list) -> None:
        [widget.delete(0, END) for widget in widgets]

    def change_state(widgets_with_state: list[(ttk.Widget, int)]) -> None:
        widget = 0
        state_of_widget = 1
        [widget_state[widget].config(state=widget_state[state_of_widget]) for widget_state in widgets_with_state]

    def accept_class(students_listbox: 'Listbox', classes_listbox: 'Listbox') -> None:
        students_listbox.delete(0, END)
        chosen_class = classes_listbox.curselection()
        if not chosen_class:
            messagebox.showerror("Error", "Please choose a class!")
        else:
            chosen_class = classes_listbox.get(chosen_class)  # convert indices into actual values
            fetch_students(students_listbox, chosen_class[0])
            global store_class_name
            store_class_name = chosen_class

    def all_parameters_given(widgets: list) -> str:
        for widget in widgets:
            if not widget:
                return messagebox.showerror("Error", "Please fill all gaps!")

    def url_exists(url: str) -> str:
        try:
            get(url)
        except exceptions.RequestException:
            return messagebox.showerror("Error", "Given website does not exist!")

    def add_student(first_name: str, surname: str, class_name: tuple, url: str) -> None:
        # make sure all parameters are given
        all_parameters_given([first_name, surname, class_name])

        # make sure the given url works
        url_exists(url)

        class_name = classes_display_add.get(class_name[0])
        insert_student(first_name, surname, class_name[0], url)
        # displaying information about adding student (temporarily)
        updated_added_label.config(text="Added successfully!")
        updated_added_label.after(3000, lambda: updated_added_label.config(text="(Updated/added class name)"))
        # erasing entry boxes so the user doesn't have to do it by himself
        erase([name_entry, surname_entry, url_entry])

    def add_class(class_name: str, classes_listbox: Listbox) -> str:
        # make sure all parameters were given
        all_parameters_given([class_name])

        exists = insert_class(class_name)
        if exists:
            return messagebox.showerror("Error", "Given class already exists!")

        # displaying information about adding class (temporarily)
        updated_added_label.config(text="Added successfully!")
        updated_added_label.after(3000, lambda: updated_added_label.config(text="(Updated/added class name)"))
        # displaying newly added class
        classes_listbox.config(state=NORMAL)  # changing state of listbox to make changes
        erase([classes_display_add, updated_added_name])
        fetch_classes(classes_display_add)
        classes_listbox.config(state=DISABLED)  # going back to an initial state

    def update_given_class(old_class_name: tuple, new_class_name: str) -> str:
        # make sure all parameters were given
        all_parameters_given([old_class_name, new_class_name])

        old_class_name = classes_display_add.get(old_class_name)
        exists = update_class_name(old_class_name[0], new_class_name)
        if exists:
            return messagebox.showerror("Error", "Given class already exists! Delete or change already existing class.")

        # displaying information about updating class (temporarily)
        updated_added_label.config(text="Updated successfully!")
        updated_added_label.after(3000, lambda: updated_added_label.config(text="(Updated/added class name)"))
        # displaying changes
        fetch_classes(classes_display_add)
        erase([updated_added_name])

    add_frame_store_function_mode = {
        1: update_given_class,
        2: add_class,
        3: add_student
    }

    def chosen_mode_add(mode: int, class_name: str, classes_listbox: Listbox) -> None:
        if mode == 1:
            update_given_class(classes_listbox.curselection(), class_name)
        elif mode == 3:
            add_class(class_name, classes_listbox)
        else:
            add_student(name_entry.get(), surname_entry.get(), classes_listbox.curselection(), url_entry.get())

    def call_delete_students(students_to_be_deleted: tuple, their_class: str) -> None:
        if their_class == "":
            messagebox.showerror("Error", "Please choose a class or click 'Accept'!")
        elif not students_to_be_deleted:
            messagebox.showerror("Error", "Please choose a student(s)!")
        # prevent attempt to delete students if there's no
        elif students_display_rem.get(students_to_be_deleted[0]) == "No students yet":
            messagebox.showerror("Error", "Please add students first!")
        else:
            answer = messagebox.askokcancel("Confirm", "Are you sure you want to delete?")
            if answer:
                # deleting from db
                students_to_be_deleted = [students_display_rem.get(student) for student in students_to_be_deleted]
                delete_students(students_to_be_deleted, their_class[0])
                # displaying information about deleting students (temporarily)
                confirm_remove.config(text="Deleted successfully!")
                confirm_remove.after(3000, lambda: confirm_remove.config(text="Confirm"))
                # displaying changes
                global store_class_name
                fetch_students(students_display_rem, store_class_name[0])

    def call_delete_class(class_name: str) -> None:
        if not class_name:
            messagebox.showerror("Error", "Please choose a class!")
        else:
            answer = messagebox.askokcancel("Confirm", "Are you sure you want to delete?")
            if answer:
                # deleting from db
                class_name = classes_display_rem.get(class_name)
                delete_class(class_name[0])
                # displaying information about deleting class (temporarily)
                confirm_remove.config(text="Deleted successfully!")
                confirm_remove.after(3000, lambda: confirm_remove.config(text="Confirm"))
                # displaying changes
                fetch_classes(classes_display_rem)

    def chosen_mode_rem(mode: int) -> None:
        if mode == 1:
            call_delete_class(classes_display_rem.curselection())
        else:
            global store_class_name
            call_delete_students(students_display_rem.curselection(), store_class_name)

    # the size of font for all listboxes
    f = font.Font(size=12)

    # creating main frame (using stored urls)
    main_frame = Frame(
        root,
        height=650,
        width=450
    )

    # creating widgets inside the main frame
    # for displaying and searching through available classes
    temp_classes = Listbox(main_frame)  # listbox used only to make a margin; it won't be considered

    scrollbar_classes = Scrollbar(
        temp_classes,
        width=12
    )

    classes = Listbox(
        temp_classes,
        selectmode="single",
        yscrollcommand=scrollbar_classes.set,
        font=f,
        width=12,
        height=11,
        highlightthickness=0,
        borderwidth=0
    )

    scrollbar_classes.config(command=classes.yview)
    # initial fulfillment of classes listbox
    fetch_classes(classes)
    # for confirming choice of class
    class_chosen_url = Button(
        main_frame,
        text="Accept",
        command=lambda: accept_class(
            students,
            classes
        )
    )

    # for searching students based on their surname within given class
    searching_surname = EntrySurname(main_frame)
    searching_surname.initial_settings("Enter surname")
    confirm_surname = Button(
        main_frame,
        text="Search",
        command=lambda: search_for_student(
            students,
            searching_surname.get(),
            store_class_name
        )
    )

    # for displaying available students within the given class
    scrollbar_students = Scrollbar(main_frame)
    students = Listbox(
        main_frame,
        selectmode="single",
        yscrollcommand=scrollbar_students.set,
        height=10,
        font=f
    )
    scrollbar_students.config(command=students.yview)
    # warning that reminds user of choosing class
    students.insert(END, "Choose class")
    # for redirecting users into the chosen student's portfolio
    go_to_url = Button(main_frame, text="Go", command=lambda: go_url(students, store_class_name))

    # going to other functionalities of the program, ie adding/updating and removing elements
    go_to_add_main = Button(main_frame, text="Add/Update", height=3, command=lambda: move(main_frame, add_frame,
                                                                                          classes_display_add))
    go_to_remove_main = Button(main_frame, text="Remove", height=3, command=lambda: move(main_frame, remove_frame,
                                                                                         classes_display_rem,
                                                                                         students_display_rem))

    # displaying main frame with its widgets on the screen
    main_frame.pack()
    main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    temp_classes.grid(column=1, row=0, rowspan=2, sticky=NSEW)
    # scrollbar_classes and classes are placed inside temp_classes
    scrollbar_classes.grid(column=0, row=0, rowspan=2, sticky=NSEW)
    classes.grid(column=1, row=0, padx=5, sticky=NSEW)
    class_chosen_url.grid(column=2, row=0, rowspan=2, sticky=NSEW)

    searching_surname.grid(column=4, row=0, sticky=NSEW)
    confirm_surname.grid(column=5, row=0, sticky=NSEW)

    scrollbar_students.grid(column=3, row=1, sticky=NSEW)
    students.grid(column=4, row=1, columnspan=2, sticky=NSEW)
    go_to_url.grid(column=6, row=0, rowspan=2, sticky=NSEW)

    go_to_add_main.grid(column=0, row=3, columnspan=4, sticky=NSEW)
    go_to_remove_main.grid(column=4, row=3, columnspan=3, sticky=NSEW)

    # creating remove functionality; remove frame
    remove_frame = Frame(root, height=650, width=450)

    # creating widgets inside the remove frame
    # creating widgets to choose whether a user wants to remove class(es) or student(s)
    rem_class_student = IntVar(remove_frame, 2)
    remove_class = Radiobutton(
        remove_frame,
        text="Classes mode",
        value=1,
        variable=rem_class_student,
        command=lambda: change_state(
            changing_state_dict["remove_class"]
        )
    )
    remove_students = Radiobutton(
        remove_frame,
        text="Students mode",
        value=2,
        variable=rem_class_student,
        command=lambda: change_state(
            changing_state_dict["remove_student"]
        )
    )

    # listboxes to choose (classes and students)
    temp_classes_rem = Listbox(remove_frame)
    classes_nav_rem = Scrollbar(temp_classes_rem)
    classes_display_rem = Listbox(temp_classes_rem, selectmode="single", yscrollcommand=classes_nav_rem.set, font=f,
                                  width=12, height=11, highlightthickness=0, borderwidth=0)
    classes_nav_rem.config(command=classes_display_rem.yview)
    # confirmation of choice of class
    class_chosen_rem = Button(remove_frame, text="Accept",
                              command=lambda: accept_class(students_display_rem, classes_display_rem))

    students_nav_rem = Scrollbar(remove_frame)
    students_display_rem = Listbox(remove_frame, selectmode="multiple", yscrollcommand=students_nav_rem.set, font=f)
    classes_nav_rem.config(command=students_display_rem.yview)

    # navigation buttons + confirm remove
    go_to_main_rem = Button(remove_frame, text="Portfolios", height=3, command=lambda: move(remove_frame, main_frame,
                                                                                            classes, students))
    go_to_add_rem = Button(remove_frame, text="Add/Update", height=3, command=lambda: move(remove_frame, add_frame,
                                                                                           classes_display_add))
    confirm_remove = Button(remove_frame, text="Confirm", height=3,
                            command=lambda: chosen_mode_rem(rem_class_student.get()))

    # placing widgets inside remove frame
    remove_class.grid(column=0, row=0, sticky=E)
    remove_students.grid(column=3, row=0, sticky=W)

    temp_classes_rem.grid(column=0, row=1, sticky=NSEW)
    # classes_nav_rem and classes_display_rem are placed inside temp_classes_rem
    classes_nav_rem.grid(column=0, row=0, sticky=NSEW)
    classes_display_rem.grid(column=1, row=0, padx=5, sticky=NSEW)
    class_chosen_rem.grid(column=1, row=1, sticky=NSEW)

    students_nav_rem.grid(column=2, row=1, sticky=NSEW)
    students_display_rem.grid(column=3, row=1, sticky=NSEW)

    go_to_main_rem.grid(column=0, row=2, sticky=NSEW)
    go_to_add_rem.grid(column=1, row=2, columnspan=2, sticky=NSEW)
    confirm_remove.grid(column=3, row=2, sticky=NSEW)

    # creating add functionality; add frame
    add_frame = Frame(root)

    # creating widgets inside add frame
    # three 'modes' of this frame
    add_mode = IntVar(add_frame, 2)
    update_class = Radiobutton(
        add_frame, 
        text="Update class", 
        value=1, 
        variable=add_mode,
        command=lambda: change_state(
            changing_state_dict["update_class"]
        )
    )
    new_class = Radiobutton(
        add_frame,
        text="New class",
        value=3,
        variable=add_mode,
        command=lambda: change_state(
            changing_state_dict["new_class"]
        )
    )
    new_student = Radiobutton(
        add_frame,
        text="New student",
        value=2,
        variable=add_mode,
        command=lambda: change_state(
            changing_state_dict["new_student"]
        )
    )

    # displaying class
    temp_classes_add = Listbox(add_frame)
    classes_nav_add = Scrollbar(temp_classes_add)
    classes_display_add = Listbox(temp_classes_add, selectmode="single", yscrollcommand=classes_nav_rem.set, font=f,
                                  width=12, height=9, highlightthickness=0, borderwidth=0)
    classes_nav_add.config(command=classes_display_add.yview)

    # entry for names of either updated class or new one
    updated_added_label = Label(add_frame, text="(Updated/added class name)")
    updated_added_name = Entry(add_frame, state=DISABLED)

    # entries for essential information about added students with his/her portfolio
    name_label = Label(add_frame, text="Name:")
    name_entry = Entry(add_frame)
    surname_label = Label(add_frame, text="Surname:")
    surname_entry = Entry(add_frame)
    url_label = Label(add_frame, text="URL:")
    url_entry = Entry(add_frame)

    # navigation buttons + make change button
    go_to_main_add = Button(add_frame, text="Portfolios", height=3, command=lambda: move(add_frame, main_frame, classes,
                                                                                         students))
    go_to_rem_add = Button(add_frame, text="Remove", height=3, command=lambda: move(add_frame, remove_frame,
                                                                                    classes_display_rem,
                                                                                    students_display_rem))
    make_change = Button(
        add_frame,
        text="Add",
        command=lambda: chosen_mode_add(
            add_mode.get(),
            updated_added_name.get(),
            classes_display_add
        )
    )

    # this dictionary contains prepared sets of objects to be used by RadioButtons
    changing_state_dict = {
        "update_class": [(name_entry, DISABLED),
                         (surname_entry, DISABLED),
                         (url_entry, DISABLED),
                         (updated_added_name, NORMAL),
                         (classes_display_add, NORMAL)
                         ],
        "new_class": [(name_entry, DISABLED),
                      (surname_entry, DISABLED),
                      (url_entry, DISABLED),
                      (updated_added_name, NORMAL),
                      (classes_display_add, DISABLED)
                      ],
        "new_student": [(name_entry, NORMAL),
                        (surname_entry, NORMAL),
                        (url_entry, NORMAL),
                        (updated_added_name, DISABLED),
                        (classes_display_add, NORMAL)
                        ],
        "remove_class": [(students_display_rem, DISABLED),
                         (class_chosen_rem, DISABLED)
                         ],
        "remove_student": [(students_display_rem, NORMAL),
                           (class_chosen_rem, NORMAL)
                           ]
    }

    # putting widgets inside add frame
    update_class.grid(column=0, row=0, sticky=NSEW)
    new_class.grid(column=1, row=0, sticky=NSEW)
    new_student.grid(column=2, row=0, sticky=NSEW)

    temp_classes_add.grid(column=0, row=1, rowspan=3, sticky=NSEW)
    # classes_nav_add and classes_display_add are placed inside temp_classes_add
    classes_nav_add.grid(column=0, row=0, sticky=NSEW)
    classes_display_add.grid(column=1, row=0, padx=5, sticky=NSEW)

    updated_added_label.grid(column=1, row=4, sticky=NSEW)
    updated_added_name.grid(column=0, row=4, sticky=NSEW)

    name_label.grid(column=1, row=1, sticky=S)
    name_entry.grid(column=1, row=2, padx=2, sticky=EW)
    surname_label.grid(column=2, row=1, sticky=S)
    surname_entry.grid(column=2, row=2, sticky=EW)
    url_label.grid(column=1, row=3, sticky=NSEW)
    url_entry.grid(column=2, row=3, sticky=EW)

    go_to_main_add.grid(column=0, row=5, columnspan=2, sticky=NSEW)
    go_to_rem_add.grid(column=2, row=5, sticky=NSEW)
    make_change.grid(column=2, row=4, sticky=NSEW)

    root.mainloop()


if __name__ == "__main__":
    # variable used to store class name after clicking "Accept"
    store_class_name = ""
    main()
