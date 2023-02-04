import sqlite3

from database_path import DATABASE

con = sqlite3.connect(DATABASE)
cur = con.cursor()

# Prompts
prompt_all_students_asc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        ORDER BY (:ordering) ASC;
"""

prompt_all_students_desc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        ORDER BY (:ordering) DESC;
"""

prompt_students_from_class_asc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        WHERE class_name = 'IIA'
        ORDER BY (:ordering) ASC;
"""

prompt_students_from_class_desc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        WHERE class_name = 'IIA'
        ORDER BY (:ordering) desc;
"""

# Filling dicts
first_name_dict = {"ordering": "first_name"}
surname_dict = {"ordering": "surname"}

# Ordered by first_name
values_ordereb_by_first_name_dict = dict()
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
transaction_first_name_desc_no_class = cur.execute(prompt_all_students_asc, first_name_dict)
values_first_name_desc_no_class = cur.fetchall()


# Ordered by surname
# From class IIIA
# In ascending order
transaction_surname_asc_class = cur.execute(prompt_students_from_class_asc, surname_dict)
values_surname_asc_class = cur.fetchall()

# In descending order
transaction_surname_desc_class = cur.execute(prompt_students_from_class_desc, surname_dict)
values_surname_desc_class = cur.fetchall()

# All students
# In ascending order
transaction_surname_asc_no_class = cur.execute(prompt_all_students_asc, surname_dict)
values_surname_asc_no_class = cur.fetchall()

# In descending order
transaction_surname_desc_no_class = cur.execute(prompt_all_students_desc, surname_dict)
values_surname_desc_no_class = cur.fetchall()


# No students fetched
prompt_given_class_doesnt_exist_first_name_asc = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    WHERE class_name = 'XIO'
    ORDER BY (:ordering) ASC;
"""

prompt_given_class_doesnt_exist_first_name_desc = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    WHERE class_name = 'XIO'
    ORDER BY (:ordering) ASC;
"""
