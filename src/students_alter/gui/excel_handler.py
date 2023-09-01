import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

from pathlib import Path

from openpyxl import Workbook

PAD_X = 10
PAD_Y = 10


class ExcelHandler(ttk.Frame):
    """Manages the creation and addition of Excel files"""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.create_spreadsheet_button = ttk.Button(self,
                                                    text="Create Spreadsheet",
                                                    command=self.create_spreadsheet
                                                    )

        self.load_spreadsheet_button = ttk.Button(self,
                                                  text="Load Spreadsheet",
                                                  command=self.load_spreadsheet
                                                  )

        self.spreadsheet_path_entry = ttk.Entry(self)
        self.spreadsheet_path_label = ttk.Label(self, text="Spreadsheet path:")

        self.position_entries_and_labels()

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

    @staticmethod
    def create_spreadsheet():
        class_name = tk.simpledialog.askstring(title="Create Spreadsheet", prompt="Type class name:")
        if class_name is not None:
            workbook = Workbook()
            sheet = workbook.active

            sheet["A1"] = "first_name"
            sheet["B1"] = "surname"
            sheet["C1"] = "url"
            sheet["E1"] = class_name

            class_name_dir = Path(__name__).resolve().parent.parent.parent.parent.parent
            class_name_spreadsheet = class_name_dir.joinpath(f"{class_name}.xlsx")
            workbook.save(filename=class_name_spreadsheet)

            message = f"""Spreadsheet created successfully!
To open the file, go to: {class_name_spreadsheet}"""
        else:
            message = "Failed to create a spreadsheet."
        info = "Spreadsheet creation status"

        return tk.messagebox.showinfo(info, message)

    def load_spreadsheet(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Excel files", "*.xlsx"),)
                                              )
        self.spreadsheet_path_entry.delete(0, tk.END)
        self.spreadsheet_path_entry.insert(0, filename)

    def position_entries_and_labels(self):
        self.create_spreadsheet_button.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)
        self.load_spreadsheet_button.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)
        self.spreadsheet_path_entry.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky=tk.EW)
        self.spreadsheet_path_label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky=tk.E)

    def return_entries_values(self):
        return self.spreadsheet_path_entry.get(),

    def erase(self):
        self.spreadsheet_path_entry.delete(0, tk.END)
