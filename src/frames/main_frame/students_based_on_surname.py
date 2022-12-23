from tkinter import messagebox, Listbox, END
from sqlite3 import connect
from ..cas_managing_db_two import fetch_class


def fetch_surname(chosen_class: str, surname: str) -> list[str]:
    c = connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """select first_name, surname from students where class_id = (:class_id) and surname = (:surname) 
    order by first_name;"""
    cur.execute(
        prompt,
        {"class_id": class_id, "surname": surname}
    )
    searching_student = cur.fetchall()
    c.close()
    return searching_student


def search_for_student(students_listbox: Listbox, surname: str, chosen_class: str):
    # check whether class was chosen
    if not chosen_class:
        return messagebox.showerror("Error", "Please choose a class or click 'Accept'!")

    # check whether there are any students with a given surname
    searching_students = fetch_surname(chosen_class[0], surname)
    students_listbox.focus_set()  # enable searching_name to reset
    if not searching_students:
        return messagebox.showerror("Error", "No students with given surname were found")

    # displaying all students whose surname meets the given one
    students_listbox.delete(0, END)
    [students_listbox.insert(END, each_found) for each_found in searching_students]
