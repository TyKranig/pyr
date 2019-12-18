#!/usr/bin/env python3
import datetime
import time
from apicall import ApiCall
from sheetwriter import SheetWriter
from dao import DataWriter

# open two cnnection to the Mongo db
gamesColl = DataWriter("games")
performancesColl = DataWriter("performances")


# IDs for seasons 1, 2, and 3 respectively as (season number, season id)
SEASONS = [(1, 10824), (2, 11086), (3, 11336)]
# games to skip that were broken or cheated
BROKEGAMES = [5036395844]

def callApi():
  gamesColl.clearData()
  performancesColl.clearData()
  
  dotaApi = ApiCall()
  for season in SEASONS:
    resp = dotaApi.getLeague(league_id=season[1])
    print("{0} matches parsing...".format(len(resp)))
    for index, k in enumerate(resp):
      print("\r{0}".format(index), end = '')
      matchId = k['match_id']
      if matchId not in BROKEGAMES:
        match = dotaApi.getMatchJson(match_id=matchId)
        gamesColl.writeOne(match[0])
        for performance in match[1]:
          performancesColl.writeOne(performance)

writer = SheetWriter("test")

topKills = performancesColl.getData("kills", 10, -1)
writer.writeArray(1, 1, topKills, "kills", "player_name", "dotabuff")

time.sleep(30)
topDeaths = performancesColl.getData("deaths", 10, -1)
writer.writeArray(12, 1, topDeaths, "deaths", "player_name", "dotabuff")

time.sleep(30)
topAssists = performancesColl.getData("assists", 10, -1)
writer.writeArray(23, 1, topAssists, "assists", "player_name", "dotabuff")

time.sleep(30)
topGPM = performancesColl.getData("gold_per_min", 10, -1)
writer.writeArray(34, 1, topGPM, "gold_per_min", "player_name", "dotabuff")

time.sleep(30)
longDuration = gamesColl.getData("duration", 5, -1)
writer.writeArray(45, 1, longDuration, "string_duration", "dotabuff")

time.sleep(30)
shortDuration = gamesColl.getData("duration", 5, 1)
writer.writeArray(51, 1, shortDuration, "string_duration", "dotabuff")
