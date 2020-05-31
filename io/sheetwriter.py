import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from lxml.html import fromstring


class SheetWriter():
    def __init__(self, sheet):
        self.scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        self.jsonCreds = os.path.join(os.path.dirname(__file__), "CDL-Sheet-18007c70b37d.json")
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.jsonCreds, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open("League-Of-Lads-Records").worksheet(sheet)

    def writeArray(self, range, data, *args):
        cells = self.sheet.range(range)
        multi = len(args)
        for rank, value in enumerate(data):
            for index, field in enumerate(args):
                cells[rank * multi + index].value = value[field]
        self.sheet.update_cells(cells)

    ### Data is an array of Tuples
    def writeArray(self, range, arr):
        cells = self.sheet.range(range)
        i = 0
        curr = arr[i]
        for index, cell in enumerate(cells):
            if index % 3 == 0 and index > 2:
                i+= 1
                curr = arr[i]
            cell.value = curr[index % 3]


        self.sheet.update_cells(cells)