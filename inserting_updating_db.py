from requests import get, exceptions
from abc import ABC, abstractmethod
from enum import Enum, auto
import sqlite3


def all_parameters_given(widgets: list) -> bool:
    for widget in widgets:
        if not widget:
            return False
    return True


def url_exists(url: str) -> bool:
    try:
        get(url)
    except exceptions.RequestException:
        return False
    return True


class AlterDB(ABC):
    """This class defines how classes altering db should look like."""

    prompts = {
        "test_existence": "select class_name from classes where class_name = (:class_name);",
        "retrieve_id": "select class_id from classes where class_name = (:class_name);",
        "insert_class": "insert into classes(class_name) values (:class_name);",
        "update_class": "select class_name from classes where class_name = (:class_name);",
        "insert_student": "insert into students values (:first_name, :surname, :class_id, :url);"
    }

    # connect to the db
    def __init__(self):
        self.c = sqlite3.connect("cas_db.db")
        self.cur = self.c.cursor()

    # functions that are either an intermediate steps or parameters checking
    def exists_in_db(self, column: str, value: str) -> bool:
        prompt = self.prompts["test_existence"]
        self.cur.execute(prompt, {column: value})
        fetched_value = self.cur.fetchone()

        if fetched_value is None:
            return False

        return True

    def fetch_class_id(self, class_name: str) -> int:
        prompt = self.prompts["retrieve_id"]
        self.cur.execute(prompt, {"class_name": class_name})
        class_id = self.cur.fetchone()[0]
        return class_id

    # ensures data is provided in the subclass's initializer and is correct
    # implementation however depends on the particular case
    @abstractmethod
    def data_is_correct(self) -> bool:
        pass

    # function that alters db
    @abstractmethod
    def insert(self) -> None:
        pass


class StudentData(Enum):
    """This class stores enum of a student's data to specify
    the order in which values in the list should be provided."""

    FIRST_NAME = auto()
    SURNAME = auto()
    URL = auto()
    CLASS_NAME = auto()


class NewStudent(AlterDB):
    """This class manages creating a student record."""

    def __init__(self,
                 first_name: StudentData.FIRST_NAME, surname: StudentData.SURNAME,
                 url: StudentData.URL, class_name: StudentData.CLASS_NAME):
        super().__init__()
        self.__first_name = first_name
        self.__surname = surname
        self.__url = url
        self.__class_name = class_name

    def data_is_correct(self) -> bool:
        if not all_parameters_given([
                self.__first_name, self.__surname,
                self.__url, self.__class_name
                ]):
            return False

        if not url_exists(self.__url):
            return False

        return True

    def insert(self) -> None:
        class_id = self.fetch_class_id(self.__class_name)
        prompt = self.prompts["insert_student"]
        self.cur.execute(prompt, {
            "first_name": self.__first_name, "surname": self.__surname,
            "url": self.__url, "class_id": class_id})
        self.c.commit()
        self.c.close()
