import sqlite3

from src.paths.database_path import DATABASE


class SQLite:
    """Manages the connection with the db.
    Attribution: https://tinyurl.com/5aph27bt"""
    def __init__(self, file=DATABASE):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type_, value, traceback):
        if traceback is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
