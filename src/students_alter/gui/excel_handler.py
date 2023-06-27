import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

from openpyxl import Workbook


class ExcelHandler(ttk.Frame):
    """Manages the creation and addition of Excel files"""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.create_spreadsheet_button = ttk.Button(self,
                                                    text="Create Spreadsheet",
                                                    command=lambda e: self.create_spreadsheet()
                                                    )

        self.load_spreadsheet_button = ttk.Button(self, text="Load Spreadsheet")

        self.spreadsheet_path_entry_var = tk.StringVar()
        self.spreadsheet_path_entry = ttk.Entry(self, textvariable=self.spreadsheet_path_entry_var)

    @staticmethod
    def create_spreadsheet():
        class_name = tk.simpledialog.askstring(title="Create Spreadsheet", prompt="Type class name:")
        workbook = Workbook()
        sheet = workbook.active

        sheet["A1"] = "first_name"
        sheet["B1"] = "surname"
        sheet["C1"] = "url"
        sheet["E1"] = class_name

        workbook.save(filename=class_name)

        return tk.messagebox.showinfo("Spreadsheet creation status", "Spreadsheet created successfully!")

    def load_spreadsheet(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Excel files", "*.xlsx"),)
                                              )
        self.spreadsheet_path_entry_var = filename
