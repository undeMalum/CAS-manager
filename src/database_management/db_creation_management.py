import sqlite3

DATABASE = "cas_portfolios.db"


def create_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""CREATE TABLE IF NOT EXISTS classes(
                    class_id INTEGER PRIMARY KEY,
                    class_name TEXT NOT NULL UNIQUE
                    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
                    student_id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    class_id INTEGER,
                    url TEXT NOT NULL,
                    FOREIGN KEY (class_id) REFERENCES classes(class_id)
                    ON DELETE CASCADE);""")

    conn.close()


if __name__ == "__main__":
    create_database(DATABASE)
