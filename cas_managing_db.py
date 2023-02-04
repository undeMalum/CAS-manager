import sqlite3
from tkinter import END, Listbox, NORMAL

# creating database with 2 table; classes and students
DATABASE = "cas_portfolios.db"
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS classes(
                class_id INTEGER PRIMARY KEY,
                class_name TEXT NOT NULL UNIQUE
                );""")

cursor.execute("""CREATE TABLE IF NOT EXISTS students(
                student_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                surname TEXT NOT NULL,
                class_id INTEGER,
                url TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
                );""")

conn.close()


# functions employing db: to be imported in main file
def fetch_classes(listbox: Listbox) -> None:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    prompt = "SELECT class_name FROM classes ORDER BY class_name;"
    cur.execute(prompt)
    available_classes = cur.fetchall()

    # it is needed to somehow simplify these if statements
    state = str(listbox["state"])  # if the state is disabled, we must change it to provide new data
    if state == "disabled":
        listbox.config(state=NORMAL)

    listbox.delete(0, END)  # clear what is currently written
    if not available_classes:  # if there are no classes, give appropriate message
        listbox.insert(END, "Add classes")
    else:
        [listbox.insert(END, each_class) for each_class in available_classes]

    listbox["state"] = state  # comeback to the original state

    c.close()


def fetch_class(class_name: str) -> int:
    """Fetches class_id based on class_name from classes table
    to use in students table"""
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    prompt = "SELECT class_id FROM classes WHERE class_name = (:class_name);"
    cur.execute(prompt, {"class_name": class_name})
    class_id = cur.fetchone()[0]
    c.close()
    return class_id


def fetch_surname(chosen_class: str, surname: str) -> list[str]:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """SELECT first_name, surname FROM students WHERE class_id = (:class_id) AND surname = (:surname) 
    ORDER BY surname;"""
    cur.execute(prompt, {"class_id": class_id, "surname": surname})
    searching_student = cur.fetchall()
    c.close()
    return searching_student


def fetch_students(students_listbox: Listbox, chosen_class: str) -> None:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = "SELECT first_name, surname FROM students WHERE class_id = (:class_id) ORDER BY surname;"
    cur.execute(prompt, {"class_id": class_id})
    available_students = cur.fetchall()
    if not available_students:
        students_listbox.delete(0, END)
        students_listbox.insert(END, "No students yet")
    else:
        [students_listbox.insert(END, each_class) for each_class in available_students]
    c.close()


def fetch_url(chosen_class: str, chosen_student: tuple[str, str]) -> str:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """SELECT url FROM students WHERE class_id = (:class_id) AND first_name = (:first_name)
    AND surname = (:surname);"""
    cur.execute(prompt, {"class_id": class_id, "first_name": chosen_student[0], "surname": chosen_student[1]})
    url = cur.fetchone()[0]
    c.close()
    return url


def insert_student(first_name: str, surname: str, chosen_class: str, url: str) -> None:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """INSERT INTO students VALUES (:first_name, :surname, :class_id, :url)"""
    cur.execute(prompt, {"first_name": first_name, "surname": surname, "class_id": class_id, "url": url})
    c.commit()
    c.close()


def exists_in_db(prompt: str, column: str, value: str) -> bool:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()

    cur.execute(prompt, {column: value})
    fetched_value = cur.fetchone()
    c.close()

    if fetched_value is None:
        return False

    return True


def insert_class(class_name: str) -> bool:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()

    prompt1 = "SELECT class_name FROM classes WHERE class_name = (:class_name)"
    if exists_in_db(prompt1, "class_name", class_name) is True:
        c.close()
        return True

    # if class of given name wasn't given
    prompt2 = "insert into classes(class_name) values (:class_name)"
    cur.execute(prompt2, {"class_name": class_name})
    c.commit()
    c.close()


def update_class_name(old_class_name: str, new_class_name: str) -> bool:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()

    prompt1 = "select class_name from classes where class_name = (:class_name)"
    if exists_in_db(prompt1, "class_name", new_class_name) is True:
        c.close()
        return True

    prompt2 = "update classes set class_name = (:new_class_name) where class_name = (:old_class_name)"
    cur.execute(prompt2, {"new_class_name": new_class_name, "old_class_name": old_class_name})
    c.commit()
    c.close()


def delete_students(students_to_be_deleted: list, their_class: str) -> None:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(their_class)
    prompt = "delete from students where class_id = (:class_id) and first_name = (:first_name) and surname = (:surname)"
    for each_student in students_to_be_deleted:
        cur.execute(prompt, {"class_id": class_id, "first_name": each_student[0], "surname": each_student[1]})
        c.commit()
    c.close()


def delete_class(class_name: str) -> None:
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    class_id = fetch_class(class_name)
    prompt1 = "delete from classes where class_id = (:class_id)"
    cur.execute(prompt1, {"class_id": class_id})
    c.commit()
    prompt2 = "delete from students where class_id = (:class_id)"
    cur.execute(prompt2, {"class_id": class_id})
    c.commit()
    c.close()
