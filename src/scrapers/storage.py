import json
import os
from scrapers.config import RAW_DATA_LOC, CLEANSED_DATA_LOC

def saveJSON(filename, datatype, data):
    dataLoc = ''
    if datatype == 'raw':
        dataLoc = RAW_DATA_LOC
    elif datatype == 'cleansed':
        dataLoc = CLEANSED_DATA_LOC

    with open(dataLoc+filename+'.json', "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def getFiles(datatype = 'raw'):
    dataLoc = ''
    if datatype == 'raw':
        dataLoc = RAW_DATA_LOC
    elif datatype == 'cleansed':
        dataLoc = CLEANSED_DATA_LOC

    files = [f for f in os.listdir(dataLoc) if f.endswith('.json')]
    filepaths = []
    for file in files:
        file_path = os.path.join(dataLoc, file)
        filepaths.append(file_path)

    return filepaths

def getJSON(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
