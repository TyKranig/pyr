import requests
import json
import pymongo
import datetime
from apicall import ApiCall

def clearCol(col):
  x = col.delete_many({})
  print(x.deleted_count, " listings deleted")

class DataWriter():
  def __init__(self, box):
    self.client = pymongo.MongoClient("mongodb://192.168.1.2:27017/")
    self.db = self.client["database"]
    self.collection = self.db[box]

  def clearData(self, box):
    clearCol(self.collection)

  def writeData(self, box, data):
    self.collection.insert_many(data)
  
  def printData(self, box):
    for game in self.collection.find().sort("duration", -1).limit(10):
      print(datetime.timedelta(seconds=game["duration"]), game["match_id"])


# IDs for seasons 1 2 and 3 respectively
leagues = [10824,11086,11336]
# games to skip that were broken
gamesSkipped = [5036395844]

# sets = []
# api = ApiCall()
# listings = api.getLeague(session, league_id=11336)['result']['matches']
# for g in listings:
#   if g["match_id"] not in gamesSkipped:
#     sets.append(api.getMatch(session, match_id=g["match_id"])["result"])

# for game in collection.find().sort("duration", -1).limit(10):
#   print(datetime.timedelta(seconds=game["duration"]), game["match_id"])

# for game in collection.find().sort("duration", 1).limit(10):
#   print(datetime.timedelta(seconds=game["duration"]), game["match_id"])
