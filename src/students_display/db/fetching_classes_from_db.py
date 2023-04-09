from src.database_management import db_manager


def fetch_class_names_from_db() -> list[tuple[str]]:
    prompt = """SELECT class_name FROM classes"""

    with db_manager.SQLite() as cur:
        cur.execute(prompt)

        return cur.fetchall()


def get_class_names() -> list[str]:
    """Prepare all available class to be displayed in combobox
     as a sorting option"""

    fetched_values = fetch_class_names_from_db()

    # The first value of classes combobox must be '-None-',
    # indicating that no class is chosen.
    class_combobox_values = ["-None-"]

    # fetched_values are in format: [('IIA',), ('IO',), ('IIB',)]
    # and must be transferred to: ['IIA', 'IO', 'IIB']
    # in class_combobox_values
    for value in fetched_values:
        class_combobox_values.append(value[0])

    return class_combobox_values


