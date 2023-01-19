from copy import copy
from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.reader.excel import load_workbook
from openpyxl.formula.translate import Translator
from openpyxl.styles import Font, Alignment


__all__ = ['Report', 'format_cell', 'formula']


def format_cell(origin: Cell, new: Cell) -> None:  # TO DO create a constant format for another cell
    """Formating input new cell by original cell"""
    new.font = copy(origin.font)
    new.alignment = copy(origin.alignment)
    new.number_format = origin.number_format


def formula(row: int, column: str) -> str:  # TO DO create a variable formula function
    """Return string with Excel formula for calculate balance"""
    return f'=Счета!{column}{row-1} + ' \
           f'SUMIFS(Транзакции!$E:$E, Транзакции!$A:$A, Счета!A{row}, Транзакции!$D:$D, Счета!${column}$1)'


class Report:
    """Work with Excel framework"""
    def __init__(self, path_to_book: str) -> None:  # Strong!
        """Set work book"""
        self._path_to_book = path_to_book
        self._book = load_workbook(path_to_book)
        self.__empty_rows = {}

    def get_book(self) -> Workbook:  # Strong!
        """Return the Excel Workbook object from path"""
        return self._book

    def get_sheet(self, sheet_name: str) -> Worksheet:  # Strong!
        """Return the Excel worksheet object from workbook by sheet name"""
        return self._book[sheet_name]

    @staticmethod
    def last_row(sheet: Worksheet) -> int:  # Strong!
        """Return number of the last not-empty row in sheet"""
        row = 1
        while True:
            if sheet[f'A{row + 1}'].value is None:
                break
            row += 1
        return row

    def empty_row(self, sheet: Worksheet) -> int:  # Strong!
        """Return and save the first empty row of sheet"""
        row = self.__empty_rows.get(str(sheet))
        if row is None:
            find = self.last_row(sheet) + 1
            self.__empty_rows[str(sheet)] = find
            return find
        else:
            return row

    @staticmethod
    def __write_transaction_row(sheet: Worksheet, transaction: list, empty_row: int) -> None:  # Nice!
        """Format empty row like pre-row and write equal transaction value"""
        if len(sheet[empty_row]) != len(transaction):
            raise ValueError("Incorrect transaction!")

        row_to_write = [i for i in sheet[empty_row]]
        example_row = [i for i in sheet[empty_row - 1]]
        for ind, empty_cell in enumerate(row_to_write):
            format_cell(example_row[ind], empty_cell)  # TO DO create a constant format for another cell
            try:
                empty_cell.value = float(transaction[ind].replace(',', '.'))
                empty_cell.number_format = '0.00 Р'
            except ValueError:
                empty_cell.value = transaction[ind]

    def write_transaction(self, sheet: Worksheet, transaction: list) -> None:  # Nice!
        """Check | find row to write transaction and do that"""
        row = self.__empty_rows.get(str(sheet))
        if row is None:
            empty_row = self.empty_row(sheet)
            self.__write_transaction_row(sheet, transaction, empty_row)
            self.__empty_rows[str(sheet)] += 1
        else:
            self.__write_transaction_row(sheet, transaction, row)
            self.__empty_rows[str(sheet)] += 1

    def save_book(self) -> None:  # Strong!
        """Save changes in book by path"""
        self._book.save(self._path_to_book)

    @staticmethod
    def __write_report_row(sheet: Worksheet, day: str, empty_row: int) -> None:  # Nice!
        """Format and fill date cell. Parse formula to another cells"""
        date_cell = sheet[empty_row][0]
        format_cell(sheet[empty_row - 1][0], date_cell)
        date_cell.value = day
        for ind, cell in enumerate(sheet[empty_row][1:], 1):
            if sheet[empty_row - 1][ind].value is None:
                break
            col = cell.column_letter
            cell.value = formula(empty_row, col)

    def write_report(self, sheet: Worksheet, day: str) -> None:  # Nice!
        """Write report of sum daily transactions"""
        row = self.__empty_rows.get(str(sheet))
        if row is None:
            empty_row = self.empty_row(sheet)
            self.__write_report_row(sheet, day, empty_row)
            self.__empty_rows[str(sheet)] += 1
        else:
            self.__write_report_row(sheet, day, row)
            self.__empty_rows[str(sheet)] += 1
