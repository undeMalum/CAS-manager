# Prompts for fetching
prompt_all_students_asc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        ORDER BY {} ASC;
"""

prompt_all_students_desc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        ORDER BY {} DESC;
"""

prompt_students_from_class_asc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        WHERE class_name = 'IIIA'
        ORDER BY {} ASC;
"""

prompt_students_from_class_desc = """
        SELECT student_id, first_name, surname, class_name
        FROM students
        INNER JOIN classes 
        ON students.class_id = classes.class_id
        WHERE class_name = 'IIIA'
        ORDER BY {} DESC;
"""

# No students fetched
prompt_given_class_doesnt_exist_first_name_asc = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    WHERE class_name = 'XIO'
    ORDER BY {} ASC;
"""

prompt_given_class_doesnt_exist_first_name_desc = """
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    WHERE class_name = 'XIO'
    ORDER BY {} ASC;
"""
