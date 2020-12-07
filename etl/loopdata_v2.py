from csv import DictReader
from json import dump
from collections import defaultdict

# detectors dictionary is "detectorid":"locationtext"
# This dictionary is to add locationtext field to loopdata
detectors = defaultdict(str)
with open("freeway_detectors.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    d_list = list(reader)
    for d in d_list:
        detectors[d["detectorid"]] = d["locationtext"]

# final list of loopdata
loopdata = list()

with open("freeway_loopdata.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    loopdata = list(reader)

# modified loopdata list
m_loopdata = list()
for l in loopdata:
    # remove the row having speed value with '' or 0
    if l["speed"] != '' and l['speed'] != '0':
        l["schema"] = "1.0"
        l["speed"] = int(l["speed"])
        l["volume"] = int(l["volume"])
        l["occupancy"] = int(l["occupancy"])
        l["status"] = int(l["status"])
        l["dqflags"] = int(l["dqflags"])
        # Add locationtext data to each loopdata
        if detectors[l['detectorid']]:
            l["locationtext"] = detectors[l["detectorid"]]
        m_loopdata.append(l)

with open("loopdata.json", 'w') as f:
    dump(m_loopdata, f)