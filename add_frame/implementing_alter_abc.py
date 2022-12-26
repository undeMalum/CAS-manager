import the_base_for_inserting_updating_db as base
import validation_descriptors


class UpdateClass(base.AlterDB):
    """This class manages changing a class record."""
    __old_class_name = validation_descriptors.UpdatingNameExists()
    __new_class_name = validation_descriptors.RepeatsInDB()

    def __init__(self, old_class_name: str, new_class_name: str):
        super().__init__()
        self.__old_class_name = old_class_name
        self.__new_class_name = new_class_name

    # altering database: updating classes
    def alter(self) -> None:
        prompt = self.prompts["update_class"]
        data = {
            "new_class_name": self.__new_class_name,
            "old_class_name": self.__old_class_name
        }
        self.cur.execute(prompt, data)


class NewClass(base.AlterDB):
    """This class manages creating a class record."""
    __class_name = validation_descriptors.RepeatsInDB()

    def __init__(self, class_name: str):
        super().__init__()
        self.__class_name = class_name

    # altering database: inserting classes
    def alter(self) -> None:
        prompt = self.prompts["insert_class"]
        data = {
            "class_name": self.__class_name
        }
        self.cur.execute(prompt, data)


class NewStudent(base.AlterDB):
    """This class manages creating a student record."""
    __first_name = validation_descriptors.DataIsGiven()
    __surname = validation_descriptors.DataIsGiven()
    __url = validation_descriptors.URLIsCorrect()
    __class_name = validation_descriptors.UpdatingNameExists()

    def __init__(self,
                 first_name: str, surname: str,
                 url: str, class_name: str):
        super().__init__()
        self.__first_name = first_name
        self.__surname = surname
        self.__url = url
        self.__class_name = class_name

    # altering database: inserting students
    def alter(self) -> None:
        class_id = self.fetch_class_id(self.__class_name)
        prompt = self.prompts["insert_student"]
        data = {
            "first_name": self.__first_name, "surname": self.__surname,
            "url": self.__url, "class_id": class_id
        }
        self.cur.execute(prompt, data)
