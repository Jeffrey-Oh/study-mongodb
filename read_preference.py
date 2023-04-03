from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
import certifi

conn = "mongodb+srv://jeffrey:qseawd12@study.nloqpdl.mongodb.net/?readPreference=secondary"
# readPreference=secondary
# -> secondary 요청으로 변경하는 옵션
client = MongoClient(conn, tlsCAFile=certifi.where())
db = client.test

db.fruits.insert_many([
    {
        "name": "melon",
        "qty" : 1000,
        "price" : 16000
    },
    {
        "name": "strawberry",
        "qty" : 100,
        "price" : 10000
    },
    {
        "name": "grape",
        "qty" : 1500,
        "price" : 5000
    }
])

query_filter = {"name" : "melon"}
while True:
    # with_options(read_preference=ReadPreference.SECONDARY)
    # -> 기본적으로 primary 쪽으로 데이터를 조회 하지만 조회를 secondary 로 주어 primary 부하를 줄인다
    res = db.fruits.find_one(query_filter)
    print(res)