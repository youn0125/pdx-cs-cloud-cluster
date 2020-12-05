from json import dump
import pandas as pd
import math
from csv import DictReader
from collections import defaultdict

# read csv file and put it into array
df = pd.read_csv('freeway_loopdata.csv', dtype={
    "detectorid": str,
    "starttime": str,
    "volume": str,
    "speed": str,
    "occupancy": str,
    "status": str,
    "dqflags": str
})

# detectors dictionary is "detectorid":"locationtext"
# This dictionary is to add locationtext field to loopdata
detectors = defaultdict(str)
with open("freeway_detectors.csv", "r", encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    d_list = list(reader)
    for d in d_list:
        detectors[d["detectorid"]] = d["locationtext"]

finalList = list()

# group by detectorid
# same detectorid's loopdata will be  divided into two
# b/c of the size limit of document(16mb)
grouped = df.groupby('detectorid')
for key, value in grouped:
    dictionary_f = dict()
    dictionary_s = dict()

    j = grouped.get_group(key).reset_index(drop=True)
    dictionary_f['detectorid'] = j.at[0, 'detectorid']
    # add locationtext to query efficiently
    if detectors[dictionary_f['detectorid']]:
        dictionary_f['locationtext'] = detectors[dictionary_f['detectorid']]
    dictionary_f['schema'] = "1.0"
    # add numlowspeed and numhighspeed to query efficiently
    dictionary_f['numlowspeed'] = 0
    dictionary_f['numhighspeed'] = 0

    dictionary_s['detectorid'] = j.at[0, 'detectorid']
    # add locationtext to query efficiently
    if detectors[dictionary_s['detectorid']]:
        dictionary_s['locationtext'] = detectors[dictionary_s['detectorid']]
    dictionary_s['schema'] = "1.0"
    # add numlowspeed and numhighspeed to query efficiently
    dictionary_s['numlowspeed'] = 0
    dictionary_s['numhighspeed'] = 0

    # list of data
    dictList = list()
    for i in j.index:
        anotherDict = dict()
        if math.isnan(float(j.at[i, 'speed'])) == False and int(j.at[i, 'speed']) != 0:
            anotherDict['starttime'] = j.at[i, 'starttime']
            anotherDict['volume'] = int(j.at[i, 'volume'])
            anotherDict['speed'] = int(j.at[i, 'speed'])
            anotherDict['occupancy'] = j.at[i, 'occupancy']
            anotherDict['status'] = j.at[i, 'status']
            anotherDict['dqflags'] = j.at[i, 'dqflags']

            dictList.append(anotherDict)

            if anotherDict['speed'] < 5:
                dictionary_f['numlowspeed'] += 1
                dictionary_s['numlowspeed'] += 1
            if anotherDict['speed'] > 80:
                dictionary_f['numhighspeed'] += 1
                dictionary_s['numhighspeed'] += 1

    if len(dictList) != 0:
        length = len(dictList)
        middle_index = length // 2
        dictionary_f['data'] = dictList[:middle_index]
        finalList.append(dictionary_f)
        dictionary_s['data'] = dictList[middle_index:]
        finalList.append(dictionary_s)

file_cnt = 0
for l in finalList:
    with open("freeway_loopdata_" + str(file_cnt) + ".json", 'w') as f:
        dump(l, f)
        file_cnt += 1