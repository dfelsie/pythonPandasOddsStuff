import json
from pprint import pprint
import csv
import pandas as pd
from rawData.constants.consts import *
import math
import numpy as np

csvFileNames=['betStuff','raptorStuff','eloStuff']

commonHeaders=['date','homeTeam','awayTeam','homeScore','awayScore','outcome']
eloHeaders=commonHeaders+['eloProbHome','eloProbAway','eloLogLoss','eloAbsDiff']
raptorHeaders=commonHeaders+['raptorProbHome','raptorProbAway','raptorLogLoss','raptorAbsDiff']
betHeaders=commonHeaders+['betProbHome','betProbAway','betLogLoss','betAbsDiff']

df=pd.read_csv('rawData/combinationfirsttry2.csv')
#print(df.sort_values(by=['raptorAbsDiff']).head(10)[betHeaders])

(df.sort_values(by=['betAbsDiff']).head(10)[betHeaders].to_csv('rawData/bonusInfobetStuffDesc.csv'))
(df.sort_values(by=['raptorAbsDiff']).head(10)[raptorHeaders].to_csv('rawData/bonusInforaptorStuffDesc.csv'))
(df.sort_values(by=['eloAbsDiff']).head(10)[eloHeaders].to_csv('rawData/bonusInfoeloStuffDesc.csv'))
(df.sort_values(by=['betAbsDiff']).tail(10)[betHeaders].to_csv('rawData/bonusInfobetStuffAsc.csv'))
(df.sort_values(by=['raptorAbsDiff']).tail(10)[raptorHeaders].to_csv('rawData/bonusInforaptorStuffAsc.csv'))
(df.sort_values(by=['eloAbsDiff']).tail(10)[eloHeaders].to_csv('rawData/bonusInfoeloStuffAsc.csv'))