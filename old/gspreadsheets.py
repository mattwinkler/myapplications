
from __future__ import print_function
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
import pandas as pd

""" Uses Google Sheets API to access a Spreadsheet and store the resulting data in a dataframe """

JSON_KEY_FILE_NAME = os.environ.get('JSON_KEY_FILE_NAME')

SCOPE = ['https://spreadsheets.google.com/feeds']

GSPREAD_CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE_NAME, SCOPE)
GSPREAD_CLIENT = gspread.authorize(GSPREAD_CREDENTIALS)

TARGET_SPREADSHEET = sys.argv[1]
TARGET_WORKSHEET = sys.argv[2]


def main():
	spreadsheet = GSPREAD_CLIENT.open(TARGET_SPREADSHEET)
	worksheet = spreadsheet.worksheet(TARGET_WORKSHEET)
	records = worksheet.get_all_records()
	df = pd.DataFrame(records)
	print(df.head())


if __name__ == '__main__':
	main()



