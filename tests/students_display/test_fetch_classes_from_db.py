import pytest

from src.students_display.db.fetching_classes_from_db import get_class_names, fetch_class_names_from_db
from src.database_management.db_manager import SQLite


@pytest.fixture
def get_classes():
    with SQLite() as cur:
        cur.execute("SELECT class_name FROM classes")
        return cur.fetchall()


@pytest.mark.fetching
def test_fetch_class_names_from_db(get_classes):
    fetched_values = fetch_class_names_from_db()

    assert fetched_values == get_classes


@pytest.mark.fetching
def test_get_class_names(get_classes):
    fetched_values = get_class_names()
    expected_values = ["-None-"] + [value[0] for value in get_classes]

    assert fetched_values == expected_values
