import os
import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials
from lxml.html import fromstring
from dotenv import load_dotenv

# Different Record Books
books = ["Midwest-Dota-2-League-Records", "League-Of-Lads-Records", "RD2L-Masters-Records"]
keys = ["cdl-sheet-70904f9e1392.json", "CDL-Sheet-18007c70b37d.json", "rd2l-masters.json"]

class SheetWriter():
    def __init__(self, sheet, league):
        load_dotenv()
        self.scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        self.jsonCreds = os.path.join(os.path.dirname(__file__), keys[league])
        self.jsonDict = {}
        self.jsonDict['type'] = os.environ.get("type")
        self.jsonDict['project_id'] = os.environ.get("project_id")
        self.jsonDict['private_key_id'] = os.environ.get("private_key_id")
        self.jsonDict['private_key'] = os.environ.get("private_key")
        self.jsonDict['client_email'] = os.environ.get("client_email")
        self.jsonDict['client_id'] = os.environ.get("client_id")
        self.jsonDict['auth_uri'] = os.environ.get("auth_uri")
        self.jsonDict['token_uri'] = os.environ.get("token_uri")
        self.jsonDict['auth_provider_x509_cert_url'] = os.environ.get("auth_provider_x509_cert_url")
        self.jsonDict['client_x509_cert_url'] = os.environ.get("client_x509_cert_url")
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.jsonDict, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open(books[league]).worksheet(sheet)

    def writeArray(self, range, data, *args):
        time.sleep(1)
        cells = self.sheet.range(range)
        multi = len(args)
        for rank, value in enumerate(data):
            for index, field in enumerate(args):
                cells[rank * multi + index].value = value[field]
        self.sheet.update_cells(cells)

    ### Data is an array of Tuples
    def writeArray(self, range, arr):
        time.sleep(1)
        cells = self.sheet.range(range)
        i = 0
        curr = arr[i]
        for index, cell in enumerate(cells):
            if index % 3 == 0 and index > 2:
                i+= 1
                curr = arr[i]
            cell.value = curr[index % 3]

        self.sheet.update_cells(cells)