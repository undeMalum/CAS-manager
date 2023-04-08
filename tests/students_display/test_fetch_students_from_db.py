import pytest

from src.students_display.db.fetching_students_from_db import get_students
from tests.students_display.fetching_predicted_values.fetch_order_by_first_name import (
    values_ordered_by_first_name_dict
)
from tests.students_display.fetching_predicted_values.fetch_order_by_surname import (
    values_ordered_by_surname_dict
)
from tests.students_display.fetching_predicted_values.fetch_no_students import (
    values_no_students_dict
)


@pytest.mark.fetching
@pytest.mark.parametrize("sorting_element, sorting_order, class_name, predicted_values", [
    ("first_name", "A-Z", "IIIA", values_ordered_by_first_name_dict["values_first_name_asc_class"]),
    ("first_name", "Z-A", "IIIA", values_ordered_by_first_name_dict["values_first_name_desc_class"]),
    ("first_name", "A-Z", "-None-", values_ordered_by_first_name_dict["values_first_name_asc_no_class"]),
    ("first_name", "Z-A", "-None-", values_ordered_by_first_name_dict["values_first_name_desc_no_class"]),
    ("surname", "A-Z", "IIIA", values_ordered_by_surname_dict["values_surname_asc_class"]),
    ("surname", "Z-A", "IIIA", values_ordered_by_surname_dict["values_surname_desc_class"]),
    ("surname", "A-Z", "-None-", values_ordered_by_surname_dict["values_surname_asc_no_class"]),
    ("surname", "Z-A", "-None-", values_ordered_by_surname_dict["values_surname_desc_no_class"])
])
def test_get_students(sorting_element: str, sorting_order: str,
                      class_name: str, predicted_values: list[(str, str)]):
    fetched_values = get_students(sorting_element, sorting_order, class_name)

    assert fetched_values == (predicted_values, "Available students")


@pytest.mark.fetching
@pytest.mark.parametrize("sorting_element, sorting_order, class_name, predicted_values", [
    ("surname", "A-Z", "XIO", values_no_students_dict["no_values_surname_asc_class"]),
    ("surname", "Z-A", "XIO", values_no_students_dict["no_values_surname_desc_class"]),
    ("first_name", "A-Z", "XIO", values_no_students_dict["no_values_first_name_asc_class"]),
    ("first_name", "Z-A", "XIO", values_no_students_dict["no_values_first_name_desc_class"])
])
def test_get_no_students(sorting_element: str, sorting_order: str,
                         class_name: str, predicted_values: list[(str, str)]):
    fetched_values = get_students(sorting_element, sorting_order, class_name)

    assert fetched_values == (predicted_values, "No students available")
