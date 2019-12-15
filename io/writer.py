#!/usr/bin/env python
import datetime
import time
from apicall import ApiCall
from sheetwriter import SheetWriter
from dao import DataWriter

# open two cnnection to the Mongo db
gamesColl = DataWriter("games")
performancesColl = DataWriter("performances")

def callApi():
  gamesColl.clearData()
  performancesColl.clearData()
  # IDs for seasons 1, 2, and 3 respectively as (season number, season id)
  seasons = [(1, 10824)]#, (2, 11086), (3, 11336)]
  # games to skip that were broken or cheated
  gamesSkipped = [5036395844]
  dotaApi = ApiCall()
  for season in seasons:
    resp = dotaApi.getLeague(league_id=season[1])
    print("{0} matches parsing...".format(len(resp)))
    for index, k in enumerate(resp):
      print("\r{0}".format(index), end = '')
      if(index > 10):
        break
      if k["match_id"] not in gamesSkipped:
        match = dotaApi.getMatch(match_id=k["match_id"])
        match["string_duration"] = str(datetime.timedelta(seconds=match["duration"]))
        match["dotabuff"] = "https://www.dotabuff.com/matches/{0}".format(k["match_id"])
        gamesColl.writeOne(match)
        for performance in match["players"]:
          # Steam api only lets you look up players with a 64bit account id, the one stored in dota is 32bit
          sixtyfour = performance["account_id"] + 76561197960265728
          performance["match_id"] = k["match_id"]
          performance["player_name"] = dotaApi.getPlayerSummary(steamids=sixtyfour)["personaname"]
          performance["dotabuff"] = "https://www.dotabuff.com/matches/{0}".format(k["match_id"])
          performancesColl.writeOne(performance)

writer = SheetWriter("test")

topKills = performancesColl.getData("kills", 10, -1)
writer.writeArray(1,1, topKills, "kills", "player_name", "dotabuff")

topDeaths = performancesColl.getData("deaths", 10, -1)
writer.writeArray(12,1, topDeaths, "deaths", "player_name", "dotabuff")

topAssists = performancesColl.getData("assists", 10, -1)
writer.writeArray(23,1, topAssists, "assists", "player_name", "dotabuff")

topGPM = performancesColl.getData("gold_per_min", 10, -1)
writer.writeArray(34,1, topGPM, "gold_per_min", "player_name", "dotabuff")

longDuration = gamesColl.getData("duration", 5, -1)
writer.writeArray(45,1, longDuration, "string_duration", "dotabuff")

shortDuration = gamesColl.getData("duration", 5, 1)
writer.writeArray(51,1, shortDuration, "string_duration", "dotabuff")

# print("updating kills")
# for i in range(6):
#     item = kHeap.pop()
#     data = getFormattedData(item, "kills")
#     sheet.update_cell(i+2, 1, data.get(POINT))
#     sheet.update_cell(i+2, 2, data.get(PLAYER_NAME))
#     sheet.update_cell(i+2, 3, data.get(DOTABUFF_URL))
# time.sleep(30)
# print("updating deaths")
# for i in range(10):
#     item = dHeap.pop() 
#     data = getFormattedData(item, "deaths")
#     sheet.update_cell(i+10, 1, data.get(POINT))
#     sheet.update_cell(i+10, 2, data.get(PLAYER_NAME))
#     sheet.update_cell(i+10, 3, data.get(DOTABUFF_URL))
# time.sleep(30)
# print("updating assists")
# for i in range(5):
#     item = aHeap.pop()
#     data = getFormattedData(item, "assists")
#     sheet.update_cell(i+23, 1, data.get(POINT))
#     sheet.update_cell(i+23, 2, data.get(PLAYER_NAME))
#     sheet.update_cell(i+23, 3, data.get(DOTABUFF_URL))
# time.sleep(30)
# print("updating gpm")
# for i in range(6):
#     item = gHeap.pop()
#     data = getFormattedData(item, "gold_per_min")
#     sheet.update_cell(i+2, 5, data.get(POINT))
#     sheet.update_cell(i+2, 6, data.get(PLAYER_NAME))
#     sheet.update_cell(i+2, 7, data.get(DOTABUFF_URL))
# time.sleep(30)
# print("duration")
# for i in range(5):
#     item = tHeap.pop()
#     data = getFormattedData(item, "duration")
#     sheet.update_cell(i+10, 5, str(datetime.timedelta(seconds=data.get(POINT))))
#     sheet.update_cell(i+10, 6, data.get(DOTABUFF_URL))
# time.sleep(30)
# print("min game")
# for i in range(5):
#     item = minGame.pop()
#     data = getFormattedData(item, "duration")
#     sheet.update_cell(i+23, 5, str(datetime.timedelta(seconds=data.get(POINT))))
#     sheet.update_cell(i+23, 6, data.get(DOTABUFF_URL))
