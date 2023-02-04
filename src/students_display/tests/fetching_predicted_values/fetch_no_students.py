import sqlite3

from database_path import DATABASE
from src.students_display.tests.fetching_predicted_values.prompts import (
    prompt_given_class_doesnt_exist_first_name_asc,
    prompt_given_class_doesnt_exist_first_name_desc
)

# !!! Note: no students will be fetched, since the given class (XIO) doesn't exist/is not added

# Connect to db
con = sqlite3.connect(DATABASE)
cur = con.cursor()

# Filling dicts
surname_dict = {"ordering": "surname"}
first_name_dict = {"ordering": "first_name"}

# Ordered by surname
# From class XIO
# In ascending order
transaction_surname_asc_class = cur.execute(prompt_given_class_doesnt_exist_first_name_asc, surname_dict)
no_values_surname_asc_class = cur.fetchall()

# In descending order
transaction_surname_desc_class = cur.execute(prompt_given_class_doesnt_exist_first_name_desc, surname_dict)
no_values_surname_desc_class = cur.fetchall()

# Ordered by first_name
# From class XIO
# In ascending order
transaction_first_name_asc_class = cur.execute(prompt_given_class_doesnt_exist_first_name_asc, first_name_dict)
no_values_first_name_asc_class = cur.fetchall()

# In descending order
transaction_first_name_desc_class = cur.execute(prompt_given_class_doesnt_exist_first_name_desc, first_name_dict)
no_values_first_name_desc_class = cur.fetchall()

# Store all values
values_no_students_dict = {
    "no_values_surname_asc_class": no_values_surname_asc_class,
    "no_values_surname_desc_class": no_values_surname_desc_class,
    "no_values_first_name_asc_class": no_values_first_name_asc_class,
    "no_values_first_name_desc_class": no_values_first_name_desc_class,
}

con.close()
