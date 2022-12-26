import implementing_alter_abc as imp
from add_modes import AddMode

from typing import Union
from collections import UserDict


class MultipleItemsDict(UserDict):
    """Modifies the behavior of dict - allows to store multiple items.

    input:
    key_and_items = [
        (AddMode.UPDATE_CLASS, (imp.UpdateClass, chosen_class, class_name))
    ]

    AddMode.UPDATE_CLASS - key
    (imp. ....) - item

    It prevents creating objects until needed.
    """
    def __getitem__(self, key):
        class_to_be_created = self.data[key][0]
        parameters = self.data[key][1:]
        return class_to_be_created(*parameters)


def create_mode_to_object_dict(chosen_class: str, class_name: str,
                               first_name: str, surname: str, url: str) -> dict[AddMode:tuple]:
    """Create dict that maps object and parameter to an appropriate mode"""
    key_and_items = {
        (AddMode.UPDATE_CLASS, (imp.UpdateClass, chosen_class, class_name)),
        (AddMode.NEW_CLASS, (imp.NewClass, class_name)),
        (AddMode.NEW_STUDENT,  (imp.NewStudent, first_name, surname, url, chosen_class))
    }
    map_mode_to_object = MultipleItemsDict(key_and_items)
    return map_mode_to_object


def alter_db(object_to_alter_db: Union[imp.NewStudent, imp.NewClass, imp.UpdateClass]) -> None:
    """Alter db with created object (depending on chosen mode)"""
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


def manage_interaction_with_db(mode: AddMode, chosen_class: str,
                               class_name: str, first_name: str,
                               surname: str, url: str) -> (str, str):
    """Handles interaction with database. It creates an objects and then alters db with it."""
    map_mode_to_object = create_mode_to_object_dict(chosen_class, class_name,
                                                    first_name, surname, url)

    try:
        object_altering_db = map_mode_to_object[mode]
    except ValueError as exc:
        return "Error", str(exc)
    else:
        alter_db(object_altering_db)
        return "Completed!", "Operation completed successfully!"
