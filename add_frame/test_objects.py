from inserting_updating_interacting_with_db import manage_interaction_with_db, create_mode_to_object_dict
import implementing_alter_abc as imp
from add_modes import AddMode
from add_frame_constants import DATABASE

import pytest
import sqlite3


@pytest.mark.dbalteration
@pytest.mark.parametrize("""chosen_class, 
                            class_name, first_name,
                            surname, url""", [
    ("n", "n", "n", "n", "n"),
    ("n", "o", "n", "n", "n"),
    ("n", "n", "n", "n", "https://undemalum.github.io/portfolio/posts/school-festival/")
])
def test_create_mode_to_object_dict(chosen_class: str,
                                         class_name: str, first_name: str,
                                         surname: str, url: str):
    mapped = create_mode_to_object_dict(
        chosen_class,
        class_name,
        first_name,
        surname,
        url
    )

    to_compare = {
        AddMode.UPDATE_CLASS: (imp.UpdateClass, chosen_class, class_name),
        AddMode.NEW_CLASS: (imp.NewClass, class_name),
        AddMode.NEW_STUDENT: (imp.NewStudent, first_name, surname, url, chosen_class)
    }

    assert mapped == to_compare


@pytest.mark.dbalteration
@pytest.mark.parametrize("""mode, chosen_class, 
                            class_name, first_name,
                            surname, url""", [
    (AddMode.NEW_CLASS, "n", "n", "n", "n", "n"),
    (AddMode.UPDATE_CLASS, "n", "o", "n", "n", "n"),
    (AddMode.NEW_STUDENT, "o", "n", "n", "n", "https://undemalum.github.io/portfolio/posts/school-festival/")
]
)
def test_manage_interaction_with_db_true(mode: AddMode, chosen_class: str,
                                         class_name: str, first_name: str,
                                         surname: str, url: str):
    mode_to_object_dict = create_mode_to_object_dict(
        chosen_class,
        class_name,
        first_name,
        surname,
        url
    )
    info, description = manage_interaction_with_db(
        mode,
        mode_to_object_dict
    )

    assert description == "Operation completed successfully!"
    assert info == "Completed!"


@pytest.mark.dbalteration
@pytest.mark.parametrize("""mode, chosen_class,
                            class_name, first_name,
                            surname, url, error_description""", [
    (AddMode.UPDATE_CLASS, "", "", "", "", "", "Choose class to be updated!"),
    (AddMode.UPDATE_CLASS, "o", "", "", "", "", "Given class already exists or is not given!"),
    (AddMode.UPDATE_CLASS, "n", "n", "", "", "", "Choose class to be updated!"),
    (AddMode.NEW_STUDENT, "n", "n", "", "", "", "Provided data is incorrect."),
    (AddMode.NEW_STUDENT, "n", "n", "n", "n", "", "Website with given url does not exist.")
]
)
def test_manage_interaction_with_db_false(mode: AddMode, chosen_class: str,
                                          class_name: str, first_name: str,
                                          surname: str, url: str, error_description):
    mode_to_object_dict = create_mode_to_object_dict(
        chosen_class,
        class_name,
        first_name,
        surname,
        url
    )
    info, description = manage_interaction_with_db(
        mode,
        mode_to_object_dict
    )
    assert info == "Error"
    assert description == error_description


@pytest.mark.dbalteration
def test_delete_from_db():
    """Delete what was added during the test"""
    c = sqlite3.connect(DATABASE)
    cur = c.cursor()
    prompt1 = """DELETE FROM students 
    WHERE class_id = 6"""
    prompt2 = """DELETE FROM classes
    WHERE class_id = 6"""
    cur.execute(prompt1)
    c.commit()
    cur.execute(prompt2)
    c.commit()
    cur.execute("SELECT * FROM students")
    print(cur.fetchall())
    cur.execute("SELECT * FROM classes")
    print(cur.fetchall())
    c.close()
