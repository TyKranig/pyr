import requests
import json
import pymongo
from apicall import ApiCall

def clearCol(col):
  x = col.delete_many({})
  print(x.deleted_count, " listings deleted")

api = ApiCall()
session = requests.Session()
listings = api.getLeague(session, league_id=11336)

client = pymongo.MongoClient("mongodb://192.168.1.2:27017/")
db = client["database"]
collection = db["games"]

clearCol(collection)
x = collection.insert_many( listings['result']['matches'] )

for game in collection.find().sort("gameid"):
  print(game)