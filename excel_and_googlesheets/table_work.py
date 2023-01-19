from copy import copy
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from openpyxl.formula.translate import Translator
from openpyxl.styles import Font, Alignment


__all__ = ['Report', 'format_cell']


def format_cell(origin, new):
    new.font = copy(origin.font)
    new.alignment = copy(origin.alignment)
    new.number_format = origin.number_format


class Report:
    """Work with Excel framework"""
    def __init__(self, path_to_book: str) -> None:
        """Set work book"""
        self.path_to_book = path_to_book
        self.book = load_workbook(path_to_book)
        self.__to_write_transaction = None
        self.__to_write_report = None

    def get_book(self) -> Workbook:
        return self.book

    def get_sheet(self, sh: str):
        return self.book[sh]

    @staticmethod
    def last_row(sheet) -> int:
        """Returns number of the last not-empty row in sheet"""
        # print('def last_row')
        i = 1
        while True:
            if sheet[f'A{i + 1}'].value is None:
                break
            i += 1
        return i

    def empty_row(self, sheet):
        # print('def empty_row')
        if self.__to_write_transaction is None:
            find = self.last_row(sheet) + 1
            self.__to_write_transaction = find
            return find
        else:
            return self.__to_write_transaction

    def __write_transaction_row(self, sheet, transaction):
        # Rewrite clear
        row_to_write = [i for i in sheet[self.__to_write_transaction]]
        example_row = [i for i in sheet[self.__to_write_transaction - 1]]
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
        if self.__to_write_transaction is None:
            self.empty_row(sheet)
            self.__write_transaction_row(sheet, transaction)
            self.__to_write_transaction += 1
        else:
            self.__write_transaction_row(sheet, transaction)
            self.__to_write_transaction += 1

    def save_book(self):
        self.book.save(self.path_to_book)

    def write_report(self, sheet, day) -> None:
        """Write report of sum daily transactions"""


