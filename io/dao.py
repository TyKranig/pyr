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
        if len(data) > 0:
            self.collection.insert_many(data)

    def writeOne(self, data):
        self.collection.insert_one(data)

    def getData(self, field, amt, sort, filter):
        return self.collection.find(filter, {"_id": 0}).sort(field, sort).limit(amt)


class GamesDao(DataWriter):
    def lookForMatch(self, matchId):
        return self.collection.find({"match_id": matchId})


class PerformancesDao(DataWriter):
    def getCaptainWins(self, match):
        pipeline = [
            match,
            {"$group": { "_id":"$account_id", "wins": {"$sum": "$win"}}},
            {"$project": {"_id": 0, "account": "$_id", "wins": "$wins"}}
        ]
        print(list(self.collection.aggregate(pipeline)))

# db.performances.aggregate([{$match: {captain: 1}},{$group: { _id:"$account_id", wins: {$sum: "$win"}}}, {$project: {_id: 0, account: "$_id", wins: "$wins"}}])
