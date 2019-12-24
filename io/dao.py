import pymongo

def clearCol(col):
  x = col.delete_many({})
  print(x.deleted_count, " listings deleted")

class DataWriter():
  def __init__(self, box):
    self.client = pymongo.MongoClient("mongodb://192.168.1.2:27017/")
    self.db = self.client["database"]
    self.collection = self.db[box]

  def clearData(self):
    x = self.collection.delete_many({})
    return x.deleted_count

  def writeMany(self, data):
    self.collection.insert_many(data)
  
  def writeOne(self, data):
    self.collection.insert_one(data)
  
  def getData(self, field, amt, sort, filter):
    return self.collection.find({},{"_id":0}).sort(field, sort).limit(amt)

# for game in collection.find().sort("duration", -1).limit(10):
#   print(datetime.timedelta(seconds=game["duration"]), game["match_id"])

# for game in collection.find().sort("duration", 1).limit(10):
#   print(datetime.timedelta(seconds=game["duration"]), game["match_id"])