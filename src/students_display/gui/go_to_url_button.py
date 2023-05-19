from tkinter import ttk

import webbrowser

from src.students_display.db import fetching_url_from_db


class URLButton(ttk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, text="GO", *args, **kwargs)

    @staticmethod
    def open_url(urls: list[str]):
        for url in urls:
            webbrowser.open(url)

    @staticmethod
    def get_url(student_id: list[int]):
        return fetching_url_from_db.fetch_url(student_id)
