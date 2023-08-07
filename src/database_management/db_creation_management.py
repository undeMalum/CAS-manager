from src.database_management.db_manager import SQLite


def create_database():

    with SQLite() as cur:
        cur.execute("PRAGMA foreign_keys = ON")

        cur.execute("""CREATE TABLE IF NOT EXISTS classes(
                        class_id INTEGER PRIMARY KEY,
                        class_name TEXT NOT NULL UNIQUE
                        );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS students(
                        student_id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        surname TEXT NOT NULL COLLATE NOCASE,
                        class_id INTEGER,
                        url TEXT NOT NULL,
                        FOREIGN KEY (class_id) REFERENCES classes(class_id)
                        ON DELETE CASCADE);""")


if __name__ == "__main__":
    create_database()
