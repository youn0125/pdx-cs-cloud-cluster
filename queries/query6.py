import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

cluster = MongoClient(MONGO_HOST,27017)
db = cluster[MONGO_DB]

# Get collection for query
col_detectors = db["Detectors"]

results = col_detectors.find({"locationtext": "Foster NB"})

for r in results:
    print(r)

