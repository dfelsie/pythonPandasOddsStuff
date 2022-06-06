import json
from pprint import pprint
import csv

# Opening JSON file
jsonDataFile = open('rawData/nbaJSON/nba/NBA.json', 'r')
data = json.load(jsonDataFile)
writeCsv = open("rawData/jsonData.csv", "w")


def moneyLineToImp(moneyLineOdds: float):
    if moneyLineOdds > 0:
        return 100/(moneyLineOdds+100)
    return (-1*(moneyLineOdds))/(-1*(moneyLineOdds)+100)


# returns JSON object as
# a dictionary


# Iterating through the json
# list
numGames = 0
dateSet = set()


with open('jsonDataFile.csv', 'w') as csvfile:

    # print(len(data["league"]["seasons"][0]["games"]))
    fieldnames = ['game_datetime', 'team_home', 'team_away', 'odds_home',
                  'odds_away', 'outcome', 'score_home', 'score_away', 'game_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data["league"]["seasons"][0]["games"]:
        if all(fieldname in i for fieldname in fieldnames):
            rowDict = {}
            for fieldName in fieldnames:
                if fieldName in ('odds_home', 'odds_away'):
                    floatMoneyLine = float(i[fieldName])
                    impOdds = moneyLineToImp(floatMoneyLine)
                    rowDict[fieldName] = impOdds
                    continue
                rowDict[fieldName] = i[fieldName]
            writer.writerow(rowdict=rowDict)

            """ numGames += 1
            if i["game_url"] in dateSet:
                print("Duplicate", i["game_url"])
            dateSet.add(i["game_url"]) """
# pprint((data["league"]["seasons"][0]["games"]))
""" for i in data['game_datetime']:
    print(i)
    writeFile.write(i) """

# Closing file
jsonDataFile.close()
