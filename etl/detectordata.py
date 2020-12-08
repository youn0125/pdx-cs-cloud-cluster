from csv import DictReader
from json import dump

# final list of detectors
detectors = list()

stations = dict()
highways = dict()

with open("freeway_detectors.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    detectors = list(reader)


with open("freeway_stations.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    s_list = list(reader)
    # Make dictionary of dictionary: stations[s_id][key] = value
    for s in s_list:
        stations[s["stationid"]] = dict()
        stations[s["stationid"]]["stationid"] = int(s["stationid"])
        stations[s["stationid"]]["upstream"] = int(s["upstream"])
        stations[s["stationid"]]["downstream"] = int(s["downstream"])
        stations[s["stationid"]]["stationclass"] = int(s["stationclass"])
        stations[s["stationid"]]["numberlanes"] = int(s["numberlanes"])
        stations[s["stationid"]]["latlon"] = s["latlon"]
        stations[s["stationid"]]["length"] = float(s["length"])



with open("highways.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    h_list = list(reader)
    # Make dictionary of dictionary: highways[h_id][key] = value
    for h in h_list:
        highways[h["highwayid"]] = dict()
        highways[h["highwayid"]]["highwayid"] = int(h["highwayid"])
        highways[h["highwayid"]]["shortdirection"] = h["shortdirection"]
        highways[h["highwayid"]]["direction"] = h["direction"]
        highways[h["highwayid"]]["highwayname"] = h["highwayname"]


for d in detectors:
    d["schema"] = "1.0"
    # Add station data to each detector
    d["station"] = stations[d["stationid"]]
    del d['stationid']
    # Add highway data to each detector
    d["highway"] = highways[d["highwayid"]]
    del d['highwayid']
    d["detectorid"] = int(d["detectorid"])
    d["milepost"] = float(d["milepost"])
    d["detectorclass"] = int(d["detectorclass"])
    d["lanenumber"] = int(d["lanenumber"])

with open("detector.json", 'w') as f:
    dump(detectors, f)