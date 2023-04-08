from src.custom_managers import db_manager
from tests.students_display.fetching_predicted_values.prompts import (
    prompt_students_from_class_asc,
    prompt_students_from_class_desc,
    prompt_all_students_asc,
    prompt_all_students_desc
)

# Filling dicts
surname = "surname"

with db_manager.SQLite() as cur:
    # Ordered by surname
    # From class IIIA
    # In ascending order
    cur.execute(prompt_students_from_class_asc.format(surname))
    values_surname_asc_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_students_from_class_desc.format(surname))
    values_surname_desc_class = cur.fetchall()

    # All students
    # In ascending order
    cur.execute(prompt_all_students_asc.format(surname))
    values_surname_asc_no_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_all_students_desc.format(surname))
    values_surname_desc_no_class = cur.fetchall()

    # Store all values
    values_ordered_by_surname_dict = {
        "values_surname_asc_class": values_surname_asc_class,
        "values_surname_desc_class": values_surname_desc_class,
        "values_surname_asc_no_class": values_surname_asc_no_class,
        "values_surname_desc_no_class": values_surname_desc_no_class,
    }
