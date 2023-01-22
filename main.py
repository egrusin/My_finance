from excel_and_googlesheets import *
from copy import copy

# TO DO remember main and transaction sheet to most useful model
# TO DO check and create directories for save Excel files

SPREADSHEET_ID = '1kuAMznNIeI9zjzDT21RloxUSOexdYS50Mmpt2V-wP50'
RANGE_NAME = 'finance!A:F'


if __name__ == '__main__':
    cur_workbook = Report('2023/1_Winter/January.xlsx')
    tempsheet = cur_workbook.get_sheet('Транзакции')

    day = get_today()
    day_transactions = get_day_transactions(SPREADSHEET_ID, RANGE_NAME, day)

    for tr in day_transactions:
        cur_workbook.write_transaction(tempsheet, tr)
    mainsheet = cur_workbook.get_sheet('Счета')

    last_report = cur_workbook.get_last_report(mainsheet)
    for date in get_diff(cur_workbook.get_last_report(mainsheet), day):
        cur_workbook.write_report(mainsheet, date)
    cur_workbook.save_book()
