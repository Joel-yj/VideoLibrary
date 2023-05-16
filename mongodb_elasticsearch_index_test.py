import pymongo
from elasticsearch import Elasticsearch, helpers
import json

client = pymongo.MongoClient('localhost',27017)
db = client['mydb']
collection = db['test']

password = "0X=9*RicED0HZvTrYrxN"

es = Elasticsearch(hosts ="https://localhost:9200",ca_certs="/Users/joel/Downloads/elasticsearch-8.6.1/config/certs/http_ca.crt",
basic_auth=("elastic", password))

res = collection.find()
num_docs = collection.count_documents({})
actions = []
for i in range(num_docs):
    doc = res[i]
    mongo_id = doc['_id']
    doc.pop('_id', None)
    actions.append({
        "_index" : "mongotest",
        "_id" : mongo_id,
        "_source": json.dumps(doc)
    })


helpers.bulk(es,actions)

