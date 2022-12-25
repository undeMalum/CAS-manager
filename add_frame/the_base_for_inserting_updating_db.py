from requests import get, exceptions
from abc import ABC, abstractmethod
import sqlite3

DATABASE = "cas_db.db"


class DataIsGiven:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.name

    def __set__(self, instance, value):
        if not value:
            raise ValueError("Provided data is incorrect.") from None
        instance.name = value


class URLIsCorrect:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.name

    def __set__(self, instance, value):
        try:
            get(value)
        except exceptions.RequestException:
            raise ValueError("Website with given url does not exist.") from None
        else:
            instance.name = value


def exists_in_db(value: str, column: str = "class_name") -> bool:
    prompt = "SElECT class_name FROM classes WHERE class_name = (:class_name);"
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    cur.execute(prompt, {column: value})
    fetched_value = cur.fetchone()

    if fetched_value is not None:
        return True
    return False


class ExistsInDB:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.name

    def __set__(self, instance, value):
        if exists_in_db(value):
            raise ValueError("Given class already exists!")
        instance.name = value


class AlterDB(ABC):
    """This class defines how classes altering db should look like."""

    prompts = {
        "test_existence": "SElECT class_name FROM classes WHERE class_name = (:class_name);",
        "retrieve_id": "SELECT class_id FROM classes WHERE class_name = (:class_name);",
        "insert_class": "INSERT INTO classes(class_name) VALUES (:class_name);",
        "update_class": "UPDATE classes SET class_name = (:new_class_name) WHERE class_name = (:old_class_name);",
        "insert_student": "INSERT INTO students VALUES (:first_name, :surname, :class_id, :url);"
    }

    # connect to the db
    def __init__(self):
        self.c = sqlite3.connect(DATABASE)
        self.cur = self.c.cursor()

    # functions that are either an intermediate steps or parameters checking
    def exists_in_db(self, value: str, column: str = "class_name") -> None:
        prompt = self.prompts["test_existence"]
        self.cur.execute(prompt, {column: value})
        fetched_value = self.cur.fetchone()

        if fetched_value is not None:
            raise ValueError("Given class already exists!")

    def fetch_class_id(self, class_name: tuple[str]) -> int:
        prompt = self.prompts["retrieve_id"]
        self.cur.execute(prompt, {"class_name": class_name})
        class_id = self.cur.fetchone()[0]
        return class_id

    def close_db(self):
        self.c.close()

    def commit(self):
        self.c.commit()

    # function that alters db
    @abstractmethod
    def alter(self) -> None:
        pass
