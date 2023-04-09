from src.database_management import db_manager
from tests.students_display.fetching_predicted_values.prompts import (
    prompt_students_from_class_asc,
    prompt_students_from_class_desc,
    prompt_all_students_asc,
    prompt_all_students_desc
)


# Filling dicts
first_name = "first_name"

with db_manager.SQLite() as cur:
    # Ordered by first_name
    # From class IIIA
    # In ascending order
    cur.execute(prompt_students_from_class_asc.format(first_name))
    values_first_name_asc_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_students_from_class_desc.format(first_name))
    values_first_name_desc_class = cur.fetchall()

    # ALl students
    # In ascending order
    cur.execute(prompt_all_students_asc.format(first_name))
    values_first_name_asc_no_class = cur.fetchall()

    # In descending order
    cur.execute(prompt_all_students_desc.format(first_name))
    values_first_name_desc_no_class = cur.fetchall()

    # Store all values
    values_ordered_by_first_name_dict = {
        "values_first_name_asc_class": values_first_name_asc_class,
        "values_first_name_desc_class": values_first_name_desc_class,
        "values_first_name_asc_no_class": values_first_name_asc_no_class,
        "values_first_name_desc_no_class": values_first_name_desc_no_class,
    }

if __name__ == "__main__":
    print(
        values_first_name_asc_class
    )
