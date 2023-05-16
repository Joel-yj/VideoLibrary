import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient('localhost',27017)
db = client['mydb']
collection = db['test']
requesting = []
count = 0

# with open('database/newdata10k.jsonl') as f:
#     for jsonObj in f:
#         myDict = json.loads(jsonObj)
#         requesting.append(InsertOne(myDict))

# result = collection.bulk_write(requesting)

for doc1 in collection.find({"video_path" : 'videos/test3.mp4'}):
    count +=1
    print(doc1)

print(count)
client.close()

