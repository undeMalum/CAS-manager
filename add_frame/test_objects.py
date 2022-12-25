import pytest
from insterting_updating_db import manage_interaction_with_db
from insterting_updating_db import AddMode


@pytest.mark.dbalteration
@pytest.mark.parametrize("""mode, chosen_class, 
                            class_name, first_name,
                            surname, url""", [
    (AddMode.UPDATE_CLASS, ("n",), "n", "n", "n", "n"),
    (AddMode.NEW_CLASS, ("n",), "n", "n", "n", "n"),
    (AddMode.NEW_STUDENT, ("n",), "n", "n", "n", "https://undemalum.github.io/portfolio/posts/school-festival/")
]
)
def test_manage_interaction_with_db_true(mode: AddMode, chosen_class: tuple[str],
                                         class_name: str, first_name: str,
                                         surname: str, url: str):
    info, description = manage_interaction_with_db(
        mode,
        chosen_class,
        class_name,
        first_name,
        surname,
        url
    )

    assert description == "Operation completed successfully!"
    assert info == "Completed!"


@pytest.mark.dbalteration
@pytest.mark.parametrize("""mode, chosen_class,
                            class_name, first_name,
                            surname, url""", [
    (AddMode.UPDATE_CLASS, ("",), "", "", "", ""),
    (AddMode.UPDATE_CLASS, ("",), "", "", "", ""),
    (AddMode.UPDATE_CLASS, ("",), "", "", "", ""),
    (AddMode.NEW_STUDENT, ("n",), "n", "n", "n", "")
]
)
def test_manage_interaction_with_db_true(mode: AddMode, chosen_class: tuple[str],
                                         class_name: str, first_name: str,
                                         surname: str, url: str):
    info, description = manage_interaction_with_db(
        mode,
        chosen_class,
        class_name,
        first_name,
        surname,
        url
    )

    assert info == "Error"
    assert description == "Operation completed successfully!"
#
#
# def test_alter_db():
#
