from pymongo import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

# 5.0 에서 기본값
# ReadConcern - local
# WriteConcern - majority

conn = "mongodb://localhost:27017,localhost:27018,localhost:27019/?w=majority&readConcernLevel=linearizable"
client = MongoClient(conn)
db = client.test

db.sales.insert_many([
    {
        "name" : "pencil",
        "price" : 10000
    },
    {
        "name" : "paper",
        "price" : 100
    },
    {
        "name" : "pen",
        "price" : 2000
    }
])

query_filter = {"price" : { "$gt" : 3000 }}
while True:
    res = db.sales.find_one(query_filter)
    print(res)