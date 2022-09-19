from tkinter import Listbox, messagebox
from webbrowser import open
from sqlite3 import connect
from ..cas_managing_db_two import fetch_class


def fetch_url(chosen_class: str, chosen_student: tuple[str, str]) -> str:
    c = connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """select url from students where class_id = (:class_id) and first_name = (:first_name)
    and surname = (:surname);"""
    cur.execute(prompt, {"class_id": class_id, "first_name": chosen_student[0], "surname": chosen_student[1]})
    url = cur.fetchone()[0]
    c.close()
    return url


def go_url(listbox_students: Listbox, chosen_class: str):
    if not chosen_class:  # check whether class was chosen
        return messagebox.showerror("Error", "Please choose a class or click 'Accept'!")

    # prevent fetching when there are no students
    selection = listbox_students.curselection()
    if not selection:  # check whether something was chosen
        return messagebox.showerror("Error", "Please choose a student or click 'Accept'!")
    elif listbox_students.get(selection) == "No students yet":  # check whether there are any students
        return messagebox.showerror("Error", "Please add students first!")

    # go to the website of a given students
    url = fetch_url(chosen_class[0], listbox_students.get(selection))
    open(url)
