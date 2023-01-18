from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
import datetime
from copy import copy
from openpyxl.styles import Font, Alignment


__all__ = ['Report', 'get_today', 'format_cell']


def format_cell(origin, new):
    new.font = Font(name=origin.font.name,
                    sz=origin.font.sz)
    new.alignment = Alignment(horizontal=origin.alignment.horizontal,
                              vertical=origin.alignment.vertical)
    new.number_format = origin.number_format
    print([new.alignment, new.font], [origin.alignment, origin.font])


def get_today() -> str:
    date = datetime.datetime.now()
    return f'{date.day}.{date.month:>02}.{date.year}'


class Report:
    """Work with Excel framework"""
    def __init__(self, path_to_book: str) -> None:
        """Set work book"""
        self.path_to_book = path_to_book
        self.book = load_workbook(path_to_book)
        self.to_write = None

    def get_book(self) -> Workbook:
        return self.book

    def get_sheet(self, sh: str):
        return self.book[sh]

    @staticmethod
    def last_row(sheet) -> int:
        # print('def last_row')
        i = 1
        while True:
            if sheet[f'A{i + 1}'].value is None:
                break
            i += 1
        return i

    def empty_row(self, sheet):
        # print('def empty_row')
        if self.to_write is None:
            find = self.last_row(sheet) + 1
            self.to_write = find
            return find
        else:
            return self.to_write

    def write_row(self, sheet, transaction):
        # print('def write_row')
        row_to_write = [i for i in sheet[self.to_write]]
        example_row = [i for i in sheet[self.to_write - 1]]
        for ind, value in enumerate(row_to_write):
            row_to_write[ind].font = copy(example_row[ind].font)
            row_to_write[ind].alignment = copy(example_row[ind].alignment)
            if ind == 4:
                row_to_write[ind].number_format = '0.00'
                row_to_write[ind].value = float(transaction[ind].replace(',', '.'))
            else:
                row_to_write[ind].number_format = example_row[ind].number_format
                row_to_write[ind].value = transaction[ind]

    def write_transaction(self, sheet, transaction: list) -> None:
        # print('def write_transaction')
        if self.to_write is None:
            self.empty_row(sheet)
            self.write_row(sheet, transaction)
            self.to_write += 1
        else:
            self.write_row(sheet, transaction)
            self.to_write += 1

    def save_book(self):
        self.book.save(self.path_to_book)



