from requests import get, exceptions
from abc import ABC, abstractmethod
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
    def exists_in_db(self, value: str, column: str = "class_name") -> bool:
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
    def alter(self) -> None:
        pass


class NewStudent(AlterDB):
    """This class manages creating a student record."""

    def __init__(self,
                 first_name: str, surname: str,
                 url: str, class_name: str):
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

    # altering database: inserting students
    def alter(self) -> None:
        class_id = self.fetch_class_id(self.__class_name)
        prompt = self.prompts["insert_student"]
        self.cur.execute(prompt, {
            "first_name": self.__first_name, "surname": self.__surname,
            "url": self.__url, "class_id": class_id})
        self.c.commit()
        self.c.close()


class NewClass(AlterDB):
    """This class manages creating a class record."""

    def __init__(self, class_name: str):
        super().__init__()
        self.__class_name = class_name

    def data_is_correct(self) -> bool:
        if not all_parameters_given([self.__class_name]):
            return False

        return True

    # altering database: inserting classes
    def alter(self) -> None:
        prompt = self.prompts["insert_class"]
        self.cur.execute(prompt, {"class_name": self.__class_name})
        self.c.commit()
        self.c.close()


class UpdateClass(AlterDB):
    """This class manages changing a class record."""

    def __init__(self, old_class_name: str, new_class_name: str):
        super().__init__()
        self.__old_class_name = old_class_name
        self.__new_class_name = new_class_name

    def data_is_correct(self) -> bool:
        if not all_parameters_given([self.__old_class_name, self.__new_class_name]):
            return False

        return True

    # altering database: updating classes
    def alter(self) -> bool:
        cur = self.c.cursor()
        if self.exists_in_db("class_name", self.__new_class_name):
            self.c.close()
            return True

        # if given class doesn't exist: update
        prompt = self.prompts["update_class"]
        cur.execute(prompt, {"new_class_name": self.__new_class_name, "old_class_name": self.__old_class_name})
        self.c.commit()
        self.c.close()
