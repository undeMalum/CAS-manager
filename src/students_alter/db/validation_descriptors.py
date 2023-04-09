from requests import get, exceptions

from src.database_management import db_manager


def exists_in_db(value: (str,), column: str = "class_name") -> bool:
    """Checks if a class of the given name exists or not"""

    prompt = "SElECT class_name FROM classes WHERE class_name = (:class_name);"

    with db_manager.SQLite() as cur:
        cur.execute(prompt, {column: value})
        fetched_value = cur.fetchone()

        if fetched_value is None:
            return False
        return True


class ValidationTemplate:
    """Implements getter (with set_name) methods for all validation descriptors"""
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class DataIsGiven(ValidationTemplate):
    """Make sure that the given string is not empty"""
    def __set__(self, instance, value):
        if not value:
            raise ValueError("Provided data is incorrect.") from None
        instance.__dict__[self.name] = value


class URLIsCorrect(ValidationTemplate):
    """Make sure that the given url exists"""
    def __set__(self, instance, value):
        try:
            get(value)
        except exceptions.RequestException:
            raise ValueError("Website with given url does not exist.") from None
        else:
            instance.__dict__[self.name] = value


class RepeatsInDB(ValidationTemplate):
    """Since classes cannot be repeated, it makes sure that a class of the given name
    does not exist yet"""
    def __set__(self, instance, value):
        if exists_in_db(value) or not value:
            raise ValueError("Given class already exists or is not given!") from None
        instance.__dict__[self.name] = value


class UpdatingNameExists(ValidationTemplate):
    """Make sure that the user chose class, that is, the old_class_name was chosen"""
    def __set__(self, instance, value):
        if not exists_in_db(value):
            raise ValueError("Choose class!") from None
        instance.__dict__[self.name] = value
