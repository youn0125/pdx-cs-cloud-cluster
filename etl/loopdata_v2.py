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
        # Add locationtext data to each loopdata
        if detectors[l['detectorid']]:
            l["locationtext"] = detectors[l["detectorid"]]
        m_loopdata.append(l)

length = len(m_loopdata)
f_index = 0
interval = length // 3
remainder = length - interval*3
# divide the loopdata into three and write three json files
for i in range(4):
    with open("loopdata_" + str(i) + ".json", 'w') as f:
        if i == 3:
            dump(m_loopdata[f_index:f_index + remainder], f)
        else:
            dump(m_loopdata[f_index:f_index + interval], f)
            f_index = f_index + interval