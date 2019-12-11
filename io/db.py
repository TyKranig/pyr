import requests
import json
import pymongo
import datetime
from apicall import ApiCall

def clearCol(col):
  x = col.delete_many({})
  print(x.deleted_count, " listings deleted")

# IDs for seasons 1 2 and 3 respectively
leagues = [10824,11086,11336]
# games to skip that were broken
gamesSkipped = [5036395844]

# sets = []
# api = ApiCall()
# session = requests.Session()
# listings = api.getLeague(session, league_id=11336)['result']['matches']
# for g in listings:
#   if g["match_id"] not in gamesSkipped:
#     sets.append(api.getMatch(session, match_id=g["match_id"])["result"])

client = pymongo.MongoClient("mongodb://192.168.1.2:27017/")
db = client["database"]
collection = db["games"]

# clearCol(collection)
# x = collection.insert_many(sets)

for game in collection.find().sort("duration", -1).limit(10):
  print(datetime.timedelta(seconds=game["duration"]), game["match_id"])

for game in collection.find().sort("duration", 1).limit(10):
  print(datetime.timedelta(seconds=game["duration"]), game["match_id"])
