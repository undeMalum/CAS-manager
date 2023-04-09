from src.database_management import db_manager

# Semicolon since it goes at the end
convert_gui_str_to_sql_asc_desc = {
    "A-Z": "ASC;",
    "Z-A": "DESC;"
}

# See the docstring for construct_dict_key
where_clause_dict = {
    "without_class-without_surname": "",
    "with_class-without_surname": "WHERE class_name = (:class_name)",
    "with_class-with_surname": "WHERE class_name = (:class_name) AND surname = (:surname)",
    "without_class-with_surname": "WHERE surname = (:surname)"
}


def construct_dict_key(class_name: str, surname: str) -> str:
    """This functions creates a key to look up in where_clause dictionary.
    This is because all required queries differ only in where clause and hence
    it is pointless to create a dictionary with entire queries as items since it
    would lead to unnecessary redundancy.

    Moreover, the choice of an appropriate query depends only on whether
    the values for class_name and surname were given or not and actual values
    doesn't matter at all.

    Taking advantage of that fact, the following query makes a test to ensure
    that the values for class_name and surname were provided (ie chosen by
    the user).

    This creates outputs:

    1. class_name = "-None-", surname = "" --> "without_class-without_surname"

    2. class_name = "IIIA", surname = "" --> "with_class-without_surname"

    3. class_name = "IIIA", surname = "Bolly" --> "with_class-with_surname"

    4. class_name = "-None-", surname = "Bolly" --> "without_class-with_surname"
    """

    with_class, with_surname = "with_class", "with_surname"
    if class_name == "-None-":
        with_class = "without_class"
    if not surname:
        with_surname = "without_surname"

    return f"{with_class}-{with_surname}"


def construct_query_for_fetching_students(sorting_element: str, sorting_order: str, where_clause_key: str) -> str:
    """
    1. where_clause_dict[where_clause_key]
        Queries differ only by where clause they have
        (see the docstring for construct_dict_key).

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
    {where_clause_dict[where_clause_key]}
    ORDER BY {sorting_element}
    {convert_gui_str_to_sql_asc_desc[sorting_order]}
    """

    return dynamic_prompt


def get_students(sorting_element: str, sorting_order: str, class_name: str, surname="") -> (list[(str, str)], str):
    """Fetches students from db to display in ttk.Treeview"""
    # Data for SQL query
    data = {
        "class_name": class_name,
        "surname": surname
    }

    # The appropriate where clause for constructing the query
    where_clause_key = construct_dict_key(class_name, surname)

    # Construct query
    prompt = construct_query_for_fetching_students(sorting_element, sorting_order, where_clause_key)

    # Handle connection with the db
    with db_manager.SQLite() as cur:
        # Perform transaction against db
        cur.execute(prompt, data)

        # Actual fetching of all values
        chosen_students = cur.fetchall()

        # If no students are added display appropriate message
        info = "Available students" if chosen_students else "No students available"

        return chosen_students, info
