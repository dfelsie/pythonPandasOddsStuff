import json
from pprint import pprint
import csv
import pandas as pd
from rawData.constants.consts import *
import math
import numpy as np

JUICE_FACTOR=1.0376507648849662

# Opening JSON file

def yesNoLogEntropy(prob1:float, prob2:float,prob1Occured:bool):
    if prob1Occured:
        return -1*math.log(prob1,2)
    return -1*math.log(prob2,2)

def absProbDiff(prob1:float, prob2:float,prob1Occured:bool):
    return abs(1-prob1) if prob1Occured else abs(1-prob2)

def nicePrintTotalLossAndAvg(name:str, logLoss:float, avg:float):
    print(name+" total: "+str(logLoss)+" avg: "+str(avg))



jsonDf=pd.read_csv('rawData/jsonData.csv')
oriCsvDf=pd.read_csv('rawData/nba_elo_short.csv')
colNames=['date','homeTeam','awayTeam','homeScore','awayScore','outcome','eloProbHome','eloProbAway','raptorProbHome','raptorProbAway','betProbHome','betProbAway','eloLogLoss','raptorLogLoss','betLogLoss','eloAbsDiff','raptorAbsDiff','betAbsDiff']
#create new ddaf with columns of jsonDf
oddsDiffTot=0
totRows=0
dictList=[]
for jsonRow in jsonDf.iterrows():
    try:
        jsonTeamHome=jsonRow[1]['team_home']
        if jsonTeamHome not in fullToShortTeamName.keys():
            continue
        jsonTeamAway=jsonRow[1]['team_away']
        jsonDate=jsonRow[1]['game_datetime'].split(' ')[0]
        shortTeamHome=fullToShortTeamName[jsonTeamHome]
        shortTeamAway=fullToShortTeamName[jsonTeamAway]
        corrOriRow=oriCsvDf[(oriCsvDf['date']==jsonDate) & (oriCsvDf['team1']==shortTeamHome) & (oriCsvDf['team2']==shortTeamAway)]
        #print(jsonTeamAway,jsonTeamHome,jsonDate, corrOriRow['team1'], corrOriRow['team2'], corrOriRow['date'])
        newRowDict={}
        newRowDict['date']=jsonDate
        newRowDict['homeTeam']=shortTeamHome
        newRowDict['awayTeam']=shortTeamAway
        newRowDict['homeScore']=jsonRow[1]['score_home']
        newRowDict['awayScore']=jsonRow[1]['score_away']
        newRowDict['outcome']=jsonRow[1]['outcome']
        newRowDict['eloProbHome']=corrOriRow['elo_prob1'].values[0]
        newRowDict['eloProbAway']=corrOriRow['elo_prob2'].values[0]
        newRowDict['raptorProbHome']=corrOriRow['raptor_prob1'].values[0]
        newRowDict['raptorProbAway']=corrOriRow['raptor_prob2'].values[0]
        oddsDiffTot+=jsonRow[1]['odds_home']
        oddsDiffTot+=jsonRow[1]['odds_away']
        betProbHome=jsonRow[1]['odds_home']/JUICE_FACTOR
        betProbAway=jsonRow[1]['odds_away']/JUICE_FACTOR
        newRowDict['betProbHome']=betProbHome
        newRowDict['betProbAway']=betProbAway
        probOneOccured=jsonRow[1]['outcome']=='HOME'
        newRowDict['eloLogLoss']=yesNoLogEntropy(newRowDict['eloProbHome'],newRowDict['eloProbAway'],probOneOccured)
        newRowDict['raptorLogLoss']=yesNoLogEntropy(newRowDict['raptorProbHome'],newRowDict['raptorProbAway'],probOneOccured)
        newRowDict['betLogLoss']=yesNoLogEntropy(betProbHome,betProbAway,probOneOccured)
        newRowDict['eloAbsDiff']=absProbDiff(newRowDict['eloProbHome'],newRowDict['eloProbAway'],probOneOccured)
        newRowDict['raptorAbsDiff']=absProbDiff(newRowDict['raptorProbHome'],newRowDict['raptorProbAway'],probOneOccured)
        newRowDict['betAbsDiff']=absProbDiff(betProbHome,betProbAway,probOneOccured)
        totRows+=1
        dictList.append(newRowDict)
        #print(pd.DataFrame(newRowDict, index=[0]))
        #pd.concat([newDf,pd.DataFrame(newRowDict,index=jsonDf.index)])
        #print(newDf)
        #pprint(newRowDict)
    #catch exception:
    except Exception as e:
        print(e)
        print("Error!")
        #break
        """ jsonTeamHome=jsonRow[1]['team_home']
        jsonTeamAway=jsonRow[1]['team_away']
        jsonDate=jsonRow[1]['game_datetime'].split(' ')[0]
        shortTeamHome=fullToShortTeamName[jsonTeamHome]
        shortTeamAway=fullToShortTeamName[jsonTeamAway]
        corrOriRow=oriCsvDf[(oriCsvDf['date']==jsonDate) & (oriCsvDf['team1']==shortTeamHome) & (oriCsvDf['team2']==shortTeamAway)]
        pprint(jsonRow[1])
        print("Error!")   """  
newDf=pd.DataFrame(dictList, columns=colNames)
newDf.to_csv('rawData/combinationfirsttry3.csv',index=False)

nicePrintTotalLossAndAvg("Elo Log Loss",newDf['eloLogLoss'].sum(),newDf['eloLogLoss'].mean())
nicePrintTotalLossAndAvg("Raptor Log Loss",newDf['raptorLogLoss'].sum(),newDf['raptorLogLoss'].mean())
nicePrintTotalLossAndAvg("Bet Log Loss",newDf['betLogLoss'].sum(),newDf['betLogLoss'].mean())
nicePrintTotalLossAndAvg("Elo Abs Diff",newDf['eloAbsDiff'].sum(),newDf['eloAbsDiff'].mean())
nicePrintTotalLossAndAvg("Raptor Abs Diff",newDf['raptorAbsDiff'].sum(),newDf['raptorAbsDiff'].mean())
nicePrintTotalLossAndAvg("Bet Abs Diff",newDf['betAbsDiff'].sum(),newDf['betAbsDiff'].mean())

    #print(jsonDate,jsonTeamHome,jsonTeamAway)
    
    #correspondingCsvRow=oriCsvDf.loc[oriCsvDf['id']==jsonRow[1]['id']]
print(oddsDiffTot/totRows)
