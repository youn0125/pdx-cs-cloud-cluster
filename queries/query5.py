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
query1 = {"locationtext": {"$regex": "^" + start + ".*" + direction, "$options" :'i' } }
query2 = {"locationtext": {"$regex": "^" + end + ".*" + direction + "$", "$options" :'i' } }

# get locationtext and downstream of start point
start_doc = col_detectors.find_one(query1, {"locationtext":1, "station.downstream": 1,"_id": 0})

# get locationtext, stationid, and downstream of end point
end_doc = col_detectors.find_one(query2, {"locationtext":1, "station.stationid":1, "station.downstream": 1,"_id": 0})

# Get all of the NB data
results = list(col_detectors.find({"locationtext": {"$regex": direction+"$", "$options":'i' }}, {"station.stationid":1, "locationtext": 1, "station.upstream": 1, "station.downstream": 1,"_id": 0}))

# save downstream of start point to find the next point
d_stream = start_doc["station"]["downstream"]
# Add start point
routes.append(start_doc["locationtext"])
for i in range(len(results)):
    depart = False
    for j in range(len(results)):
        # When finding previous point's downstream == stationid, add locationtext to routes
        # update the downstream
        # if updated downstream == end point's, ends of travel
        if d_stream == results[j]["station"]["stationid"]:
            routes.append(results[j]["locationtext"])
            d_stream = results[j]["station"]["downstream"]
            if d_stream == end_doc["station"]["stationid"]:
                depart = True
                break
            break
    if(depart == True):
        break

# Add end point
routes.append(end_doc["locationtext"])

# Display
for route in routes:
    print(route)




