#!/usr/bin/env python
import os
import json
import heapq
import datetime
import requests
import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials
from apicall import ApiCall
from lxml.html import fromstring

##############################  UTILITIES  #####################

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = 'x'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

session = requests.Session()

POINT = "point"
PLAYER_NAME = "player-name"
DOTABUFF_URL = "dotabuff-url"
def getFormattedData(item, dataPoint):
  ret = {}
  ret[POINT] = item[dataPoint]
  try:
    sixtyfour = item["account_id"] + 76561197960265728
    ret[PLAYER_NAME] = dotaApi.getPlayerSummary(session, steamids=sixtyfour)["personaname"]
  except KeyError:
    pass
  ret[DOTABUFF_URL] = "https://www.dotabuff.com/matches/{0}".format(item["match_id"])
  return ret

############################### CLASSES #######################
class DctObj(object):
  def __init__(self, key, dct):
    self.key = key
    self.dct = dct

  def __lt__(self, other):
    return self.key > other.key

  def __eq__(self, other):
    return self.key == other.key

  def __repr__(self):
    return '{0.__class__.__name__}(key={0.key}, dct={0.dct})'.format(self)

  def __str__(self):
    return json.dumps(self.dct)

class MHeap(object):
  def __init__(self):
    self._values = []

  def push(self, key, item):
    heapq.heappush(self._values, DctObj(key, item))
  
  def pop(self):
    return heapq.heappop(self._values).dct

################################  AUTH  #######################
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

jsonCreds = os.path.join(os.path.dirname(__file__), "CDL-Sheet-18007c70b37d.json")
credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonCreds, scope)
client = gspread.authorize(credentials)

sheet = client.open("CDL-Record-Book").sheet1

##############################  DATA COLLECT  #################

kHeap = MHeap()
tHeap = MHeap()
dHeap = MHeap()
aHeap = MHeap()
gHeap = MHeap()
minGame = MHeap()

# IDs for seasons 1 2 and 3 respectively
leagues = [10824,11086,11336]
# games to skip that were broken
gamesSkipped = [5036395844]

dotaApi = ApiCall()
for id in leagues:
  resp = dotaApi.getLeague(session, league_id=id)
  amt = len(resp['result']['matches'])
  print("{0} matches parsed...".format(amt))
  
  i = 0
  for k in resp['result']['matches']:
    i += 1
    printProgressBar(i, amt)
    if k["match_id"] not in gamesSkipped:
      game = dotaApi.getMatch(session, match_id=k["match_id"])["result"]  
      tHeap.push(game["duration"], game)
      minGame.push((-1 * game["duration"]), game)

      for p in game["players"]:
        # where p is the json object for a player
        p["match_id"] = k["match_id"]
        kHeap.push(p["kills"], p)
        aHeap.push(p["assists"], p)
        gHeap.push(p["gold_per_min"], p)
        dHeap.push(p["deaths"], p)

######################################## OUTPUT DATA TO SHEET ####################################3

print("updating kills")
row = 2
for i in range(6):
    item = kHeap.pop()
    data = getFormattedData(item, "kills")
    sheet.update_cell(i+2, 1, data.get(POINT))
    sheet.update_cell(i+2, 2, data.get(PLAYER_NAME))
    sheet.update_cell(i+2, 3, data.get(DOTABUFF_URL))
time.sleep(30)
print("updating deaths")
for i in range(10):
    item = dHeap.pop() 
    data = getFormattedData(item, "deaths")
    sheet.update_cell(i+10, 1, data.get(POINT))
    sheet.update_cell(i+10, 2, data.get(PLAYER_NAME))
    sheet.update_cell(i+10, 3, data.get(DOTABUFF_URL))
time.sleep(30)
print("updating assists")
for i in range(5):
    item = aHeap.pop()
    data = getFormattedData(item, "assists")
    sheet.update_cell(i+23, 1, data.get(POINT))
    sheet.update_cell(i+23, 2, data.get(PLAYER_NAME))
    sheet.update_cell(i+23, 3, data.get(DOTABUFF_URL))
time.sleep(30)
print("updating gpm")
for i in range(6):
    item = gHeap.pop()
    data = getFormattedData(item, "gold_per_min")
    sheet.update_cell(i+2, 5, data.get(POINT))
    sheet.update_cell(i+2, 6, data.get(PLAYER_NAME))
    sheet.update_cell(i+2, 7, data.get(DOTABUFF_URL))
time.sleep(30)
print("duration")
for i in range(5):
    item = tHeap.pop()
    data = getFormattedData(item, "duration")
    sheet.update_cell(i+10, 5, str(datetime.timedelta(seconds=data.get(POINT))))
    sheet.update_cell(i+10, 6, data.get(DOTABUFF_URL))
time.sleep(30)
print("min game")
for i in range(5):
    item = minGame.pop()
    data = getFormattedData(item, "duration")
    sheet.update_cell(i+23, 5, str(datetime.timedelta(seconds=data.get(POINT))))
    sheet.update_cell(i+23, 6, data.get(DOTABUFF_URL))
