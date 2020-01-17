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
        return list(self.collection.find({"match_id": matchId}))


class PerformancesDao(DataWriter):
    def getWins(self, match):
        pipeline = [
            match,
            {"$group": {
                "_id": "$account_id",
                "name": {"$last": "$steamName"},
                "wins": {"$sum": "$win"},
                "total": {"$sum": 1}
            }},
            {"$project": {"_id": 0, "account": "$_id", "wins": 1, "name": 1, "total": 1}},
            {"$sort": {"wins": -1}},
            {"$limit": 10}
        ]
        top = list(self.collection.aggregate(pipeline))
        for player in top:
            player["dotabuff"] = "https://www.dotabuff.com/players/%d" % (player["account"])
        return top

    def getWinPercentage(self, match):
        pipeline = [
            match,
            {"$group": {
                "_id": "$account_id",
                "name": {"$last": "$steamName"},
                "wins": {"$sum": "$win"},
                "total": {"$sum": 1}
            }},
            {"$project": {"_id": 0, "account": "$_id", "wins": 1, "name": 1, "total": 1, "winpercentage": {"$divide": ["$wins","$total"]}}},
            {"$sort": {"winpercentage": -1}},
            {"$limit": 10}
        ]
        top = list(self.collection.aggregate(pipeline))
        for player in top:
            player["dotabuff"] = "https://www.dotabuff.com/players/%d" % (player["account"])
        return top


if __name__ == "__main__":
    dao = PerformancesDao("performances")
    print(dao.getWinPercentage({"$match": {}}))
