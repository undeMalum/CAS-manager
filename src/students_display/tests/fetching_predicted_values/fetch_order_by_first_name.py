import sqlite3

from database_path import DATABASE
from src.students_display.tests.fetching_predicted_values.prompts import (
    prompt_students_from_class_asc,
    prompt_students_from_class_desc,
    prompt_all_students_asc,
    prompt_all_students_desc
)

# Connect to db
con = sqlite3.connect(DATABASE)
cur = con.cursor()

# Filling dicts
first_name_dict = {"ordering": "first_name"}

# Ordered by first_name
# From class IIIA
# In ascending order
transaction_first_name_asc_class = cur.execute(prompt_students_from_class_asc, first_name_dict)
values_first_name_asc_class = cur.fetchall()

# In descending order
transaction_first_name_desc_class = cur.execute(prompt_students_from_class_desc, first_name_dict)
values_first_name_desc_class = cur.fetchall()

# ALl students
# In ascending order
transaction_first_name_asc_no_class = cur.execute(prompt_all_students_asc, first_name_dict)
values_first_name_asc_no_class = cur.fetchall()

# In descending order
transaction_first_name_desc_no_class = cur.execute(prompt_all_students_desc, first_name_dict)
values_first_name_desc_no_class = cur.fetchall()

# Store all values
values_ordered_by_first_name_dict = {
    "values_first_name_asc_class": values_first_name_asc_class,
    "values_first_name_desc_class": values_first_name_desc_class,
    "values_first_name_asc_no_class": values_first_name_asc_no_class,
    "values_first_name_desc_no_class": values_first_name_desc_no_class,
}

con.close()
