import pymongo
from bson import json_util

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "lianjia"


def init_client():
    connection = pymongo.MongoClient(
        MONGODB_SERVER,
        MONGODB_PORT
    )
    return connection, connection[MONGODB_DB]


def get_districts():
    connection, db = init_client()
    districts = db.districts.find({})
    connection.close()
    return json_util.dumps(list(districts))


def get_sum(location):
    connection, db = init_client()
    _sum = db.sum.find({"location": location})
    connection.close()
    return json_util.dumps(list(_sum))

