import json
from datetime import datetime
from elasticsearch import Elasticsearch , helpers

password = "0X=9*RicED0HZvTrYrxN"

es = Elasticsearch(hosts ="https://localhost:9200",ca_certs="/Users/joel/Downloads/elasticsearch-8.6.1/config/certs/http_ca.crt",
basic_auth=("elastic", password))

def get_data_from_json(self):
    return [l.strip() for l in open(str(self), encoding= 'utf8', errors = 'ignore')]

docs = get_data_from_json("database/newdata1k.jsonl")
print("String docs length:", len(docs))

doclist = []

for num, doc in enumerate(docs):
    try:
        # doc = doc.replace("T","true")
        # doc = doc.replace("F","false")
        dict_doc = json.loads(doc)
        # dict_doc["timestamp"] = datetime.now()
        dict_doc["_id"] = num
        doclist += [dict_doc]
    except json.decoder.JSONDecodeError as err:
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)
        print ("Dict docs length:", len(doclist))
    try:
        print("\nAttempting to index the list of docs using helpers.bulk()")
        resp = helpers.bulk(
        es,
        doclist,
        index = "some_index1k"
        )
    # print the response returned by Elasticsearch
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

    except Exception as err:

        # print any errors returned w
        ## Prerequisite while making the helpers.bulk() API call
        print("Elasticsearch helpers.bulk() ERROR:", err)
        quit()


resp = es.search(index= 'some_index1k', size = 100, query={"match_all": {}})


# print the number of docs in index
print ("Length of docs returned by search():", len(resp['hits']['hits']))

for hit in resp['hits']['hits']:
    print("%(video_path)s" % hit["_source"])
