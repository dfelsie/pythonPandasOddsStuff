import math


def yesNoLogEntropy(prob1:float, prob2:float,prob1Occured:bool):
    if prob1Occured:
        return -1*math.log(prob1,2)
    return -1*math.log(prob2,2)

def absProbDiff(prob1:float, prob2:float,prob1Occured:bool):
    return abs(1-prob1) if prob1Occured else abs(1-prob2)

eloProbHome=0.49116631218891554
eloProbAway=0.5088336878110844
raptorProbHome=0.42716470119799416
raptorProbAway=0.5728352988020058
betProbHome=0.6027732893960203
betProbAway=0.3949653192027521

print("Elo:",yesNoLogEntropy(eloProbHome,eloProbAway,True))
print("Raptor:",yesNoLogEntropy(raptorProbHome,raptorProbAway,True))
print("Bet:",yesNoLogEntropy(betProbHome,betProbAway,True))
print("Elo:",absProbDiff(eloProbHome,eloProbAway,True))
print("Raptor:",absProbDiff(raptorProbHome,raptorProbAway,True))
print("Bet:",absProbDiff(betProbHome,betProbAway,True))