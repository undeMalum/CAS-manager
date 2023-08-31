import pytest

from src.students_display.db.fetching_students_from_db import (
    construct_query_for_fetching_students,
    construct_dict_key
)

prompt_template_asc_surname = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    {}
    ORDER BY surname
    ASC;
    """

prompt_template_desc_surname = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    {}
    ORDER BY surname
    DESC;
    """

prompt_template_asc_first_name = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    {}
    ORDER BY first_name
    ASC;
    """

prompt_template_desc_first_name = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    {}
    ORDER BY first_name
    DESC;
    """


Without_classWithout_surname = ""
With_classWithout_surname = "WHERE class_name = (:class_name)"
With_classWith_surname = "WHERE class_name = (:class_name) AND surname LIKE 'Bolly%'"
Without_classWith_surname = "WHERE surname LIKE 'Bolly%'"


@pytest.mark.constructing
@pytest.mark.parametrize("class_name, surname, predicted_where_clause", [
    ("-None-", "", Without_classWithout_surname),
    ("IIIA", "", With_classWithout_surname),
    ("IIIA", "Bolly", With_classWith_surname),
    ("-None-", "Bolly", Without_classWith_surname)
])
def test_construct_dict_key(class_name: str, surname: str, predicted_where_clause: str):
    where_clause = construct_dict_key(class_name, surname)

    assert where_clause == predicted_where_clause


@pytest.mark.constructing
@pytest.mark.parametrize("sorting_element, sorting_order, dict_key, predicted_query", [
    ("surname", "A-Z", Without_classWithout_surname,
     prompt_template_asc_surname.format(Without_classWithout_surname)),

    ("surname", "Z-A", Without_classWithout_surname,
     prompt_template_desc_surname.format(Without_classWithout_surname)),

    ("surname", "A-Z", With_classWithout_surname,
     prompt_template_asc_surname.format(With_classWithout_surname)),

    ("surname", "Z-A", With_classWithout_surname,
     prompt_template_desc_surname.format(With_classWithout_surname)),

    ("surname", "A-Z", With_classWith_surname,
     prompt_template_asc_surname.format(With_classWith_surname)),

    ("surname", "Z-A", With_classWith_surname,
     prompt_template_desc_surname.format(With_classWith_surname)),

    ("surname", "A-Z", Without_classWith_surname,
     prompt_template_asc_surname.format(Without_classWith_surname)),

    ("surname", "Z-A", Without_classWith_surname,
     prompt_template_desc_surname.format(Without_classWith_surname))
])
def test_construct_query_for_fetching_students_by_surname(sorting_element: str, sorting_order: str,
                                                          dict_key: str, predicted_query: str):
    constructed_query = construct_query_for_fetching_students(sorting_element, sorting_order, dict_key)

    assert constructed_query == predicted_query


@pytest.mark.constructing
@pytest.mark.parametrize("sorting_element, sorting_order, dict_key, predicted_query", [
    ("first_name", "A-Z", Without_classWithout_surname,
     prompt_template_asc_first_name.format(Without_classWithout_surname)),

    ("first_name", "Z-A", Without_classWithout_surname,
     prompt_template_desc_first_name.format(Without_classWithout_surname)),

    ("first_name", "A-Z", With_classWithout_surname,
     prompt_template_asc_first_name.format(With_classWithout_surname)),

    ("first_name", "Z-A", With_classWithout_surname,
     prompt_template_desc_first_name.format(With_classWithout_surname)),

    ("first_name", "A-Z", With_classWith_surname,
     prompt_template_asc_first_name.format(With_classWith_surname)),

    ("first_name", "Z-A", With_classWith_surname,
     prompt_template_desc_first_name.format(With_classWith_surname)),

    ("first_name", "A-Z", Without_classWith_surname,
     prompt_template_asc_first_name.format(Without_classWith_surname)),

    ("first_name", "Z-A", Without_classWith_surname,
     prompt_template_desc_first_name.format(Without_classWith_surname))
])
def test_construct_query_for_fetching_students_by_first_name(sorting_element: str, sorting_order: str,
                                                             dict_key: str, predicted_query: str):
    constructed_query = construct_query_for_fetching_students(sorting_element, sorting_order, dict_key)

    assert constructed_query == predicted_query
