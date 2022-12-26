import pytest
from implementing_alter_abc import NewStudent, NewClass, UpdateClass


@pytest.mark.validation
@pytest.mark.parametrize("first_name, surname, url, class_name", [
    ("", "", "", ""),
    ("a", "", "", ""),
    ("a", "b", "", ""),
    ("a", "b", "c", "")
])
def test_invalid_input_student(first_name, surname, url, class_name):
    # url raises different exception, and it should be caught as well
    with pytest.raises(ValueError):
        new_student = NewStudent(first_name, surname, url, class_name)


@pytest.mark.validation
def test_invalid_input_new_class():
    with pytest.raises(ValueError):
        new_student = NewClass("")


@pytest.mark.validation
@pytest.mark.parametrize("old_class_name, new_class_name", [
    ("", ""),
    ("a", ""),
    ("", "a")
])
def test_invalid_input_update_class(old_class_name, new_class_name):
    with pytest.raises(ValueError):
        new_student = UpdateClass(old_class_name, new_class_name)
