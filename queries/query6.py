import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")

MONGO_DB = os.getenv("MONGO_DB")

# connect to cluster
cluster = MongoClient(MONGO_HOST, 27017)
db = cluster[MONGO_DB]

# Get collection for query
col_detectors = db["Detectors"]

results = col_detectors.find({"locationtext": "Foster NB"})

print("Display the data before updating milepost")
for r in results:
    print(r)
    col_detectors.update_one({"milepost":r.get("milepost")}, {"$set":{"milepost": "18.1"}})

results = col_detectors.find({"locationtext": "Foster NB"})

print("Display the data after updating milepost to 30.0")
for r in results:
    print(r)