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

# Get collection for query
col_detectors = db["Detectors"]

start = "johnson cr"
end = "Powell"
direction = "NB"
start_re = re.compile(start, re.IGNORECASE)
end_re = re.compile(end, re.IGNORECASE)

routes = list()


# use $options:'i' to make the query case-insensitive
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