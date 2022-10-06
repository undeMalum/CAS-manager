import sqlite3
from tkinter import END, Listbox, NORMAL, messagebox

# creating database with 2 table; classes and students
conn = sqlite3.connect("cas_db.db")
cursor = conn.cursor()

cursor.execute("""create table if not exists classes(
                class_id integer primary key,
                class_name text not null unique
                );""")

cursor.execute("""create table if not exists students(
                first_name text not null,
                surname text not null,
                class_id integer,
                url text not null,
                foreign key (class_id) references classes(class_id)
                );""")

conn.close()


# functions employing db: to be imported in main file
def fetch_classes(listbox: Listbox) -> None:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    prompt = "select class_name from classes order by class_name;"
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
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    prompt = "select class_id from classes where class_name = (:class_name);"
    cur.execute(prompt, {"class_name": class_name})
    class_id = cur.fetchone()[0]
    c.close()
    return class_id


def fetch_surname(chosen_class: str, surname: str) -> list[str]:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """select first_name, surname from students where class_id = (:class_id) and surname = (:surname) 
    order by first_name;"""
    cur.execute(prompt, {"class_id": class_id, "surname": surname})
    searching_student = cur.fetchall()
    c.close()
    return searching_student


def fetch_students(students_listbox: Listbox, chosen_class: str) -> None:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = "select first_name, surname from students where class_id = (:class_id) order by surname;"
    cur.execute(prompt, {"class_id": class_id})
    available_students = cur.fetchall()
    if not available_students:
        students_listbox.delete(0, END)
        students_listbox.insert(END, "No students yet")
    else:
        [students_listbox.insert(END, each_class) for each_class in available_students]
    c.close()


def fetch_url(chosen_class: str, chosen_student: tuple[str, str]) -> str:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """select url from students where class_id = (:class_id) and first_name = (:first_name)
    and surname = (:surname);"""
    cur.execute(prompt, {"class_id": class_id, "first_name": chosen_student[0], "surname": chosen_student[1]})
    url = cur.fetchone()[0]
    c.close()
    return url


class AddUpdate:
    """This class stores all actions performed against the database
    that includes changing existing or adding new records"""

    prompts = {
        "teste_existence": "select class_name from classes where class_name = (:class_name);",
        "retrieve_id": "select class_id from classes where class_name = (:class_name);",
        "insert_class": "insert into classes(class_name) values (:class_name);",
        "update_class": "select class_name from classes where class_name = (:class_name);",
        "insert_student": "insert into students values (:first_name, :surname, :class_id, :url);"
    }

    def __int__(self):
        self.c = sqlite3.connect("cas_db.db")
        self.cur = self.c.cursor()

    # functions that are used either to check something or as an intermediate
    def exists_in_db(self, column: str, value: str) -> bool:
        prompt = self.prompts["test_existence"]
        self.cur.execute(prompt, {column: value})
        fetched_value = self.cur.fetchone()

        if fetched_value is None:
            return False

        return True

    # probably to be moved to another class
    def fetch_class(self, class_name: str) -> int:
        prompt = self.prompts["retrieve_id"]
        self.cur.execute(prompt, {"class_name": class_name})
        class_id = self.cur.fetchone()[0]
        return class_id

    # altering database
    def insert_class(self, class_name: str) -> bool:
        if self.exists_in_db("class_name", class_name) is True:
            self.c.close()
            return True

        # if given class doesn't exist: insert
        prompt = self.prompts["insert_class"]
        self.cur.execute(prompt, {"class_name": class_name})
        self.c.commit()
        self.c.close()

    def update_class_name(self, old_class_name: str, new_class_name: str) -> bool:
        if self.exists_in_db("class_name", new_class_name) is True:
            self.c.close()
            return True

        # if given class doesn't exist: update
        prompt = self.prompts["update_class"]
        self.cur.execute(prompt, {"new_class_name": new_class_name, "old_class_name": old_class_name})
        self.c.commit()
        self.c.close()

    def insert_student(self, first_name: str, surname: str, chosen_class: str, url: str) -> None:
        class_id = fetch_class(chosen_class)
        prompt = self.prompts["insert_student"]
        self.cur.execute(prompt, {"first_name": first_name, "surname": surname, "class_id": class_id, "url": url})
        self.c.commit()
        self.c.close()


def insert_student(first_name: str, surname: str, chosen_class: str, url: str) -> None:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(chosen_class)
    prompt = """insert into students values (:first_name, :surname, :class_id, :url)"""
    cur.execute(prompt, {"first_name": first_name, "surname": surname, "class_id": class_id, "url": url})
    c.commit()
    c.close()


def exists_in_db(prompt: str, column: str, value: str) -> bool:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()

    cur.execute(prompt, {column: value})
    fetched_value = cur.fetchone()
    c.close()

    if fetched_value is None:
        return False

    return True


def insert_class(class_name: str) -> bool:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()

    prompt1 = "select class_name from classes where class_name = (:class_name)"
    if exists_in_db(prompt1, "class_name", class_name) is True:
        c.close()
        return True

    # if class of given name wasn't given
    prompt2 = "insert into classes(class_name) values (:class_name)"
    cur.execute(prompt2, {"class_name": class_name})
    c.commit()
    c.close()


def update_class_name(old_class_name: str, new_class_name: str) -> bool:
    c = sqlite3.connect("cas_db.db")
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
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(their_class)
    prompt = "delete from students where class_id = (:class_id) and first_name = (:first_name) and surname = (:surname)"
    for each_student in students_to_be_deleted:
        cur.execute(prompt, {"class_id": class_id, "first_name": each_student[0], "surname": each_student[1]})
        c.commit()
    c.close()


def delete_class(class_name: str) -> None:
    c = sqlite3.connect("cas_db.db")
    cur = c.cursor()
    class_id = fetch_class(class_name)
    prompt1 = "delete from classes where class_id = (:class_id)"
    cur.execute(prompt1, {"class_id": class_id})
    c.commit()
    prompt2 = "delete from students where class_id = (:class_id)"
    cur.execute(prompt2, {"class_id": class_id})
    c.commit()
    c.close()
