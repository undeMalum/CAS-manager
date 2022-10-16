from requests import get, exceptions
from abc import ABC, abstractmethod
import sqlite3

DATABASE = "cas_db.db"


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
        self.c = sqlite3.connect(DATABASE)
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

    def close_db(self):
        self.c.close()

    def commit(self):
        self.c.commit()

    # static methods
    @staticmethod
    def all_parameters_given(widgets: list[str]) -> bool:
        for widget in widgets:
            if not widget:
                return False
        return True

    @staticmethod
    def url_exists(url: str) -> bool:
        try:
            get(url)
        except exceptions.RequestException:
            return False
        return True

    # ensures data is provided in the subclass's initializer and is correct
    # implementation however depends on the particular case
    @abstractmethod
    def data_is_correct(self) -> bool:
        pass

    # function that alters db
    @abstractmethod
    def alter(self) -> None:
        pass
