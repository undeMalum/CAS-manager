from the_base_for_inserting_updating_db import AlterDB, URLIsCorrect, DataIsGiven


class UpdateClass(AlterDB):
    """This class manages changing a class record."""
    __old_class_name = DataIsGiven()
    __new_class_name = DataIsGiven()

    def __init__(self, old_class_name: tuple[str], new_class_name: str):
        super().__init__()
        self.__old_class_name = old_class_name
        self.__new_class_name = new_class_name

    # altering database: updating classes
    def alter(self) -> None:
        prompt = self.prompts["update_class"]
        self.cur.execute(prompt, {"new_class_name": self.__new_class_name, "old_class_name": self.__old_class_name})


class NewClass(AlterDB):
    """This class manages creating a class record."""
    __class_name = DataIsGiven()

    def __init__(self, class_name: str):
        super().__init__()
        self.__class_name = class_name

    # altering database: inserting classes
    def alter(self) -> None:
        prompt = self.prompts["insert_class"]
        self.cur.execute(prompt, {"class_name": self.__class_name})


class NewStudent(AlterDB):
    """This class manages creating a student record."""
    __first_name = DataIsGiven()
    __surname = DataIsGiven
    __url = URLIsCorrect()
    __class_name = DataIsGiven()

    def __init__(self,
                 first_name: str, surname: str,
                 url: str, class_name: tuple[str]):
        super().__init__()
        self.__first_name = first_name
        self.__surname = surname
        self.__url = url
        self.__class_name = class_name

    # altering database: inserting students
    def alter(self) -> None:
        class_id = self.fetch_class_id(self.__class_name)
        prompt = self.prompts["insert_student"]
        self.cur.execute(prompt, {
            "first_name": self.__first_name, "surname": self.__surname,
            "url": self.__url, "class_id": class_id})
