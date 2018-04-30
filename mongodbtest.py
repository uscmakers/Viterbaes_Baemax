from pymongo import MongoClient
import json
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://apetranik:lOgseLjFbC9X9Bks@baemax-s3so4.mongodb.net/test")
db=client.admin
db=client.test

healthdata = {"activity": 10000,
	"sleep": 8,
	"heartrate": 72}

randomperson2 = {"activity": 238409,
	"sleep": 5,
	"heartrate": 84}

myperson = db.myperson
#healthdata_id = myperson.insert_one(healthdata).inserted_id
healthdata_id = myperson.insert_one(randomperson2).inserted_id
# print(healthdata_id)

# print(db.collection_names(include_system_collections=False))

for post in db.myperson.find().sort('activity', -1).limit(1):
	print(post['activity'])
	print(post['sleep'])
	print(post['heartrate'])

# print(myCursor.size)

# cursor = myCursor[0]
# for cursor in myCursor:
# print(cursor['activity'])
# myCursor.forEach(printjson)

# print(myCursor.activity)
# print(myCursor.sleep)
# print(myCursor.heartrate)

# print(myperson.find_ones())

# intents = ["activity", "sleep", "heartrate"]
# ids = [1, 2, 3]

# thing = {
# 	'intent': intents[0],
# 	'id': ids[0]
# }

# result = db.health.insert_one(thing)
# print("INSERTED: " + result)

# # Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)