from excel_and_googlesheets import *
from copy import copy


SPREADSHEET_ID = '1kuAMznNIeI9zjzDT21RloxUSOexdYS50Mmpt2V-wP50'
RANGE_NAME = 'finance!A:F'


if __name__ == '__main__':
    cur_workbook = Report('2023/1_Winter/January.xlsx')
    tempsheet = cur_workbook.get_sheet('Транзакции')

    day = get_today()
    day_transactions = get_day_transactions(SPREADSHEET_ID, RANGE_NAME, day)

    # print(day_transactions)
    for tr in day_transactions:
        cur_workbook.write_transaction(tempsheet, tr)

    mainsheet = cur_workbook.get_sheet('Счета')
    cur_workbook.write_report(mainsheet)

    cur_workbook.save_book()




