#!/usr/bin/env python3
import datetime
import time
from sheetwriter import SheetWriter
from dao import DataWriter
from dataObjects import Season, Match, CDL

SEASONS = [(1, 10824, "Season1"), (2, 11086, "Season2"), (3, 11336, "Season3")]

# open two cnnection to the Mongo db
gamesColl = DataWriter("games")
performancesColl = DataWriter("performances")

def buildDatabaseClean():
  print("clearing data")
  gamesColl.clearData()
  performancesColl.clearData()
  cdl = CDL(SEASONS)
  for season in cdl.seasons:
    gamesColl.writeMany(season.matches)
    performancesColl.writeMany(season.formatPerformances())

buildDatabaseClean()

# write seasonal records
for season in SEASONS:
  writer = SheetWriter(season[2])

  topKills = performancesColl.getData("kills", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(1, 1, topKills, "kills", "player_name", "dotabuff")

  time.sleep(30)
  topDeaths = performancesColl.getData("deaths", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(12, 1, topDeaths, "deaths", "player_name", "dotabuff")

  time.sleep(30)
  topAssists = performancesColl.getData("assists", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(23, 1, topAssists, "assists", "player_name", "dotabuff")

  time.sleep(30)
  topGPM = performancesColl.getData("gold_per_min", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(34, 1, topGPM, "gold_per_min", "player_name", "dotabuff")

  time.sleep(30)
  longDuration = gamesColl.getData("duration", 5, -1, {"seasonNumber": season[0]})
  writer.writeArray(45, 1, longDuration, "string_duration", "dotabuff")

  time.sleep(30)
  shortDuration = gamesColl.getData("duration", 5, 1, {"seasonNumber": season[0]})
  writer.writeArray(51, 1, shortDuration, "string_duration", "dotabuff")


  writer = SheetWriter("AllTime")

  topKills = performancesColl.getData("kills", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(1, 1, topKills, "kills", "player_name", "dotabuff")

  time.sleep(30)
  topDeaths = performancesColl.getData("deaths", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(12, 1, topDeaths, "deaths", "player_name", "dotabuff")

  time.sleep(30)
  topAssists = performancesColl.getData("assists", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(23, 1, topAssists, "assists", "player_name", "dotabuff")

  time.sleep(30)
  topGPM = performancesColl.getData("gold_per_min", 10, -1, {"seasonNumber": season[0]})
  writer.writeArray(34, 1, topGPM, "gold_per_min", "player_name", "dotabuff")

  time.sleep(30)
  longDuration = gamesColl.getData("duration", 5, -1, {"seasonNumber": season[0]})
  writer.writeArray(45, 1, longDuration, "string_duration", "dotabuff")

  time.sleep(30)
  shortDuration = gamesColl.getData("duration", 5, 1, {"seasonNumber": season[0]})
  writer.writeArray(51, 1, shortDuration, "string_duration", "dotabuff")