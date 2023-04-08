from src.custom_managers import db_manager
from tests.students_display.fetching_predicted_values.prompts import (
    prompt_given_class_doesnt_exist_first_name_asc,
    prompt_given_class_doesnt_exist_first_name_desc
)

# !!! Note: no students will be fetched, since the given class (XIO) doesn't exist/is not added

# Filling dicts
surname = "surname"
first_name = "first_name"

with db_manager.SQLite() as cur:
    # Ordered by surname
    # From class XIO
    # In ascending order
    cur.execute(prompt_given_class_doesnt_exist_first_name_asc.format(surname))
    no_values_surname_asc_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_given_class_doesnt_exist_first_name_desc.format(surname))
    no_values_surname_desc_class = cur.fetchall()

    # Ordered by first_name
    # From class XIO
    # In ascending order
    cur.execute(prompt_given_class_doesnt_exist_first_name_asc.format(first_name))
    no_values_first_name_asc_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_given_class_doesnt_exist_first_name_desc.format(first_name))
    no_values_first_name_desc_class = cur.fetchall()

    # Store all values
    values_no_students_dict = {
        "no_values_surname_asc_class": no_values_surname_asc_class,
        "no_values_surname_desc_class": no_values_surname_desc_class,
        "no_values_first_name_asc_class": no_values_first_name_asc_class,
        "no_values_first_name_desc_class": no_values_first_name_desc_class,
    }
