import pymongo
import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DB = os.getenv("MONGO_DB")

# connect to cluster
cluster = MongoClient(MONGO_HOST, 27017)
db = cluster[MONGO_DB]

query = db.Loopdata.aggregate(
  [
    {
      "$match": {
        "$and": [
          {"starttime" : {"$regex": "2011-09-15.*"}
          },
          {"locationtext" : "Foster NB"
          }
        ]
      }
    },
    {
      "$group": {
        "_id": 0,
        "Total volume:": {
          "$sum": "$volume"
        }
      }
    }
  ]
)
print(list(query))