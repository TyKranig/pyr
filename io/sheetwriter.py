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
    self.sheet = self.client.open("CDL-Record-Book").worksheet("Sheet2")

  def writeArray(self, x, y, data, *args):
    for rank, value in enumerate(data):
      for index, field in enumerate(args):
        self.sheet.update_cell(x + rank, y + index, value[field])