import sqlite3

from database_path import DATABASE

prompts = {
    "fetch_all_students": """SELECT student_id, first_name, surname, class_name
                              FROM students
                              INNER JOIN classes 
                              ON students.class_id = classes.class_id
                              ORDER BY (:sorting_element)""",
    "fetch_students_from_class": """SELECT student_id, first_name, surname, class_name
                                     FROM students
                                     INNER JOIN classes 
                                     ON students.class_id = classes.class_id
                                     WHERE class_name = (:class_name)
                                     ORDER BY (:sorting_element)"""
}

# Semicolon since it goes at the end
convert_gui_str_to_sql_asc_desc = {
    "A-Z": " ASC;",
    "Z-A": " DESC;"
}


def construct_query_for_fetching_students(sorting_order: str, class_name: str) -> str:
    # If no class is chosen (ie class_name is set to '-None-') display all students.
    if class_name == "-None-":
        prompt_without_sorting_order = prompts["fetch_all_students"]
    else:
        prompt_without_sorting_order = prompts["fetch_students_from_class"]

    # User can choose if he/she wants to display students in descending or ascending order.
    # However, since there's no way to implement a query for optional ASC and DESC,
    # this query needs to be constructed on the fly.
    prompt_with_sorting_order = prompt_without_sorting_order + convert_gui_str_to_sql_asc_desc[sorting_order]

    return prompt_with_sorting_order


def get_students(sorting_element: str, sorting_order: str, class_name: str) -> (list[(str, str)], str):
    """Fetches students from db to display in ttk.Treeview"""
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Data for SQL query
    data = {
        "sorting_element": sorting_element,
        "class_name": class_name
    }

    # construct query
    prompt = construct_query_for_fetching_students(sorting_order, class_name)

    # Perform transaction against db
    cur.execute(prompt, data)

    # Actual fetching of all values
    chosen_students = cur.fetchall()

    # if no students are added display appropriate message
    info = "Available students" if chosen_students else "No students available"

    return chosen_students, info
