import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from lxml.html import fromstring

class SheetWriter():
  scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
  jsonCreds = os.path.join(os.path.dirname(__file__), "CDL-Sheet-18007c70b37d.json")
  credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonCreds, scope)
  client = gspread.authorize(credentials)

  def __init__(self, sheet):
    self.sheet = client.open("CDL-Record-Book").sheet1

  def writeLine(self, x, y, **args):
    for value in args:
      self.sheet(x, y, value)
      y += 1