from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['CapstoneProject']
collection = db['Registration']

for x in collection.find():
  print(x)
