from typing import Union

from src.add_frame_package.db import implementing_alter_abc as imp
from src.add_frame_package import add_modes


def create_mode_to_object_dict(chosen_class: str, class_name: str, student_id: int,
                               first_name: str, surname: str, url: str) -> dict[add_modes.AddMode:tuple]:
    """Create dict that maps object and parameter to an appropriate mode"""
    map_mode_to_object = {
        add_modes.AddMode.UPDATE_CLASS: (imp.UpdateClass, chosen_class, class_name),
        add_modes.AddMode.NEW_CLASS: (imp.NewClass, class_name),
        add_modes.AddMode.UPDATE_STUDENT: (imp.UpdateStudent, student_id, first_name, surname, url, chosen_class),
        add_modes.AddMode.NEW_STUDENT:  (imp.NewStudent, first_name, surname, url, chosen_class)
    }
    return map_mode_to_object


def alter_db(object_to_alter_db: Union[imp.NewStudent, imp.NewClass, imp.UpdateClass]) -> None:
    """Alter db with created object (depending on chosen mode)"""
    object_to_alter_db.alter()
    object_to_alter_db.commit()
    object_to_alter_db.close_db()


def manage_interaction_with_db(mode: add_modes.AddMode,
                               map_mode_to_object: dict[add_modes.AddMode: tuple]) -> (str, str):
    """Handles interaction with database. It creates an objects and then alters db with it."""

    class_to_be_called = map_mode_to_object[mode][0]
    parameters_to_be_used = map_mode_to_object[mode][1:]

    try:
        object_altering_db = class_to_be_called(*parameters_to_be_used)
    except ValueError as exc:
        return "Error", str(exc)
    else:
        alter_db(object_altering_db)
        return "Completed!", "Operation completed successfully!"
