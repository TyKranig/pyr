import pymongo


def clearCol(col):
    x = col.delete_many({})
    print(x.deleted_count, " listings deleted")


class DataWriter():
    def __init__(self, box):
        self.client = pymongo.MongoClient("mongodb://192.168.1.6:27017/")
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
        return self.collection.find(filter, {"_id": 0}).sort(field, sort).limit(amt)

# TODO turn this into a better filter method like above
    def lookForMatch(self, matchId):
        return self.collection.find({"match_id": matchId})
