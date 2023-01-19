from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

__all__ = ['get_day_transactions']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def day_filter(massive: list[list], day: str) -> list[list]:
    """Returns daily transactions"""
    transactions = []
    for transaction in massive:
        if not transaction:
            continue

        tr_date = transaction[0].split(' ')[0]
        if tr_date == day:
            transaction[0] = tr_date
            transactions.append(transaction)
    return transactions


def get_day_transactions(sheet_id, range_sheet, day):
    """Shows basic usage of the Sheets API.
    :returns values from a finance spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range_sheet).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        return day_filter(values, day)

    except HttpError as err:
        print(err)
