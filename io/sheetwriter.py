import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from lxml.html import fromstring

# Different Record Books
books = ["Midwest-Dota-2-League-Records", "League-Of-Lads-Records", "RD2L-Masters-Records"]
keys = ["cdl-sheet-70904f9e1392.json", "CDL-Sheet-18007c70b37d.json", "rd2l-masters.json"]

class SheetWriter():
    def __init__(self, sheet, league):
        self.scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        self.jsonCreds = os.path.join(os.path.dirname(__file__), keys[league])
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.jsonCreds, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open(books[league]).worksheet(sheet)

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