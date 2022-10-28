import json
import os
import pandas as pd

# Read dir cleanData
mainPath = 'cleanData'

periods = ["5-2022", "1-2022", "2-2022", "4-2022", "3-2022", "6-2022", "7-2022", "8-2022", "9-2022", "10-2022",
           "11-2022", "12-2022"]

# Get all files in dir
files = os.listdir(mainPath)

names = json.load(open('list.json', 'r', encoding="utf-8"))


def getNameDip(id):
    for name in names:
        if name["Id"] == id:
            return name["Name"]
    return "unknown"


def getPartido(id):
    for name in names:
        if name["Id"] == id:
            partido = name["Partido"]
            if "Partido: " in partido:
                partido = partido.replace("Partido: ", "")
                return partido
    return "unknown"

def joinPaths(paths):
    res = ''
    for path in paths:
        res = os.path.join(res, path)
    return res


def forEachPeriod(filterPeriod, handler):
    # Loop through files
    for dirCleanData in files:
        # Read directoryes
        name = getNameDip(dirCleanData)
        partido = getPartido(dirCleanData)
        try:
            for dirDip in os.listdir(joinPaths([mainPath, dirCleanData])):
                # Read files
                for file in os.listdir(joinPaths([mainPath, dirCleanData, dirDip])):
                    if dirDip != filterPeriod:
                        continue
                    # Read file
                    with open(joinPaths([mainPath, dirCleanData, dirDip, file]), 'r', encoding="utf-8") as f:
                        # read json
                        data = json.load(f)
                        handler(data, name, partido)

        except NotADirectoryError:
            pass


# save dataframe

for period in periods:

    headers = dict()

    headers["Name"] = 0
    headers["Partido"] = 0


    def handlerHeader(data, name, par):
        # Create dataframe
        try:
            df = pd.DataFrame(data)
            for index, row in df.iterrows():
                key = row["Key"]
                headers[key] = 0
        except:
            print("Error")


    forEachPeriod(period, handlerHeader)

    frame = pd.DataFrame(columns=headers.keys())


    def getIndex(key):
        return list(headers.keys()).index(key)


    def handlerBody(data, name, partido):
        # Create dataframe
        # fill dataframe
        val = []
        for key in headers:
            val.append(0)

        try:
            for d in data:
                key = d["Key"]
                value = d["Value"]
                d = str.replace(value, ".", "")
                val[getIndex(key)] = d
        except:
            print("Error")

        val[getIndex("Name")] = name
        val[getIndex("Partido")] = partido

        frame.loc[len(frame.index)] = val


    forEachPeriod(period, handlerBody)

    frame.to_csv('data-' + period + '.csv', index=False)
