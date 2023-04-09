from tkinter import ttk

import webbrowser

from src.students_display.db import fetching_url_from_db


class URLButton(ttk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, text="GO", *args, **kwargs)

    @staticmethod
    def open_url(url: str):
        webbrowser.open(url)

    @staticmethod
    def get_url(student_id: int):
        return fetching_url_from_db.fetch_url(student_id)
