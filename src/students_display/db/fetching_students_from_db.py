from src.database_management import db_manager

# Semicolon since it goes at the end
convert_gui_str_to_sql_asc_desc = {
    "A-Z": "ASC;",
    "Z-A": "DESC;"
}


def construct_where_clause(class_name: str, surname: str) -> (str, str):
    """
    Created search condition.

    Checks whether any class was given or not. If so, it adds search for class name
    to the condition.

    Same with surname. Checks whether any surname was given or not. If so, it adds
    search for surname pattern to the condition.

    If none of the above condition is satisfied, returns and empty string.
    """

    and_needed_dict = {True: "AND", False: ""}
    and_needed = True

    with_class, with_surname = "class_name = (:class_name)", f"surname LIKE '{surname}%'"
    if class_name == "-None-":
        and_needed = False
        with_class = ""
    if not surname:
        and_needed = False
        with_surname = ""

    condition = f"{with_class} {and_needed_dict[and_needed]} {with_surname}".strip()  # construct temp condition

    return f"WHERE {condition}" if with_class or with_surname else ""  # if condition is needed, add where clause


def construct_query_for_fetching_students(sorting_element: str, sorting_order: str, where_clause: str) -> str:
    """
    1. where_clause
        Insert search condition if needed. Depends on
        the user input.

    2. convert_gui_str_to_sql_asc_desc[sorting_order]
        User can choose if he/she wants to display
        students in descending or ascending order.

        However, since there's no way to implement a query
        for optional ASC and DESC, this query needs to be
        constructed on the fly.
    """

    dynamic_prompt = f"""
    SELECT student_id, first_name, surname, class_name
    FROM students
    INNER JOIN classes 
    ON students.class_id = classes.class_id
    {where_clause}
    ORDER BY {sorting_element}
    {convert_gui_str_to_sql_asc_desc[sorting_order]}
    """

    return dynamic_prompt


def get_students(sorting_element: str, sorting_order: str, class_name: str, surname="") -> (list[(str, str)], str):
    """Fetches students from db to display in ttk.Treeview"""
    # Data for SQL query
    data = {
        "class_name": class_name
    }

    # The appropriate where clause for constructing the query
    where_clause = construct_where_clause(class_name, surname)

    # Construct query
    prompt = construct_query_for_fetching_students(sorting_element, sorting_order, where_clause)

    # Handle connection with the db
    with db_manager.SQLite() as cur:
        # Perform transaction against db
        cur.execute(prompt, data)

        # Actual fetching of all values
        chosen_students = cur.fetchall()

        # If no students are added display appropriate message
        info = "Available students" if chosen_students else "No students available"

        return chosen_students, info


if __name__ == "__main__":
    concant = construct_where_clause("-None-", "")
    print(concant)
