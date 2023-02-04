import pytest

from src.students_display.db.fetching_from_db import construct_query_for_fetching_students

predicted_query_with_class_asc = """SELECT student_id, first_name, surname, class_name
                                     FROM students
                                     INNER JOIN classes 
                                     ON students.class_id = classes.class_id
                                     WHERE class_name = (:class_name)
                                     ORDER BY (:sorting_element) ASC;"""
predicted_query_with_class_desc = """SELECT student_id, first_name, surname, class_name
                                     FROM students
                                     INNER JOIN classes 
                                     ON students.class_id = classes.class_id
                                     WHERE class_name = (:class_name)
                                     ORDER BY (:sorting_element) DESC;"""
predicted_query_without_class_asc = """SELECT student_id, first_name, surname, class_name
                              FROM students
                              INNER JOIN classes 
                              ON students.class_id = classes.class_id
                              ORDER BY (:sorting_element) ASC;"""
predicted_query_without_class_desc = """SELECT student_id, first_name, surname, class_name
                              FROM students
                              INNER JOIN classes 
                              ON students.class_id = classes.class_id
                              ORDER BY (:sorting_element) DESC;"""


@pytest.mark.constructing
@pytest.mark.parametrize("sorting_order, class_name, predicted_query", [
    ("A-Z", "1al", predicted_query_with_class_asc),
    ("Z-A", "1al", predicted_query_with_class_desc),
    ("A-Z", "-None-", predicted_query_without_class_asc),
    ("Z-A", "-None-", predicted_query_without_class_desc)
])
def test_construct_query_for_fetching_students(sorting_order: str, class_name: str,
                                               predicted_query: str):
    constructed_query = construct_query_for_fetching_students(sorting_order, class_name)

    assert constructed_query == predicted_query
