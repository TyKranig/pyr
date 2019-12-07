import pymongo

client = pymongo.MongoClient("mongodb://192.168.1.2:27017/")

print(print(client.list_database_names()))

db = client["mydatabase"]