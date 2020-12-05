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
milepost = "18.1"

print("\n\n---- Display the data before updating milepost ----")
for r in results:
    print("milepost:", r["milepost"])
    col_detectors.update_one({"milepost":r.get("milepost")}, {"$set":{"milepost": milepost}})

results = col_detectors.find({"locationtext": "Foster NB"})

print("\n\n---- Display the data after updating milepost to " + milepost + " ----")
for r in results:
    print("milepost", r["milepost"])