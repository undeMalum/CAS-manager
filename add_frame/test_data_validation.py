import pytest
import requests
from implementing_alter_abc import NewStudent, NewClass, UpdateClass


@pytest.mark.parametrize("first_name, surname, url, class_id", [
    ("", "", "", ("",)),
    ("a", "", "", ("",)),
    ("a", "b", "", ("",)),
    ("a", "b", "c", ("",))
])
def test_validate_input_student(first_name, surname, url, class_id):
    # url raises different exception, and it should be caught as well
    with pytest.raises((ValueError, requests.exceptions.RequestException)):
        new_student = NewStudent(first_name, surname, url, class_id)


def test_validate_input_new_class():
    with pytest.raises(ValueError):
        new_student = NewClass("")


@pytest.mark.parametrize("old_class_name, new_class_name", [
    (("",), ""),
    (("a",), "")
])
def test_validate_input_update_class(old_class_name, new_class_name):
    with pytest.raises(ValueError):
        new_student = UpdateClass(old_class_name, new_class_name)
