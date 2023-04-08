import pytest

from src.students_display.db.fetching_classes_from_db import get_class_names, fetch_class_names_from_db


@pytest.mark.fetching
def test_fetch_class_names_from_db():
    fetched_values = fetch_class_names_from_db()
    expected_values = [('IIIA',), ('IC',), ('IIB',), ('IA',), ('IO',)]

    assert fetched_values == expected_values


@pytest.mark.fetching
def test_get_class_names():
    fetched_values = get_class_names()
    expected_values = ['-None-', 'IIIA', 'IC', 'IIB', 'IA', 'IO']

    assert fetched_values == expected_values
