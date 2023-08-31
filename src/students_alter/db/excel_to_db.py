from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule

from src.students_alter.db import implementing_alter_abc as imp


def transfer_spreadsheet_to_db(file_path: Path):
    workbook = load_workbook(file_path)
    sheet = workbook.active
    sheet["D1"] = "added"

    for row, student_ex in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
        try:
            student_db = imp.NewStudent(
                student_ex[0],
                student_ex[1],
                student_ex[2],
                sheet["E1"]
            )
        except ValueError:
            sheet[f"D{row+1}"] = "no"
        else:
            student_db.alter()
            sheet[f"D{row+1}"] = "yes"

    red_background = PatternFill(fgColor="00FF0000")
    diff_style = DifferentialStyle(fill=red_background)
    rule = Rule(type="expression", dxf=diff_style)
    rule.formula = ["$D1=no"]
    sheet.conditional_formatting.add(rule)
    workbook.save(file_path)
