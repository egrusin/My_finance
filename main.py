from excel_and_googlesheets import *

# TO DO remember main and transaction sheet to most useful model
# TO DO check and create directories for save Excel files
# TO DO add minus for pay-transactions automatically
# TO DO create a functions for main procedure

SPREADSHEET_ID = '1kuAMznNIeI9zjzDT21RloxUSOexdYS50Mmpt2V-wP50'
RANGE_NAME = 'finance!A:F'


if __name__ == '__main__':
    cur_workbook = Report('2023/1_Winter/January.xlsx')
    tempsheet = cur_workbook.get_sheet('Транзакции')
    mainsheet = cur_workbook.get_sheet('Счета')

    today = get_today()
    last_transaction_date = cur_workbook.get_last_report(tempsheet)
    days = get_diff(last_transaction_date, today)

    day_transactions = get_day_transactions(SPREADSHEET_ID, RANGE_NAME, days)

    for tr in day_transactions:
        cur_workbook.write_transaction(tempsheet, tr)

    for date in get_diff(cur_workbook.get_last_report(mainsheet), today):
        cur_workbook.write_report(mainsheet, date)

    cur_workbook.save_book()
