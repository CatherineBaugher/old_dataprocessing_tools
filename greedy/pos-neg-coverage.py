#!/usr/bin/env python
import csv
import operator
import pprint
import sys
from copy import copy


#GREEDY SELECTION FNS BELOW
#------------------------------
#evalResults: given a dictionary of seqs mapped to predictions
#             determine results of the evaluation (FN, TN, FP, TP, error, accuracy etc)
def evalResults(dictofseqs,givendat,picked):
    falsepos = falseneg = truepos = trueneg = lowmiss = lowoccur = 0
    for x in range (1,len(givendat)):
        if(givendat[x][0] in dictofseqs):
            if(dictofseqs[givendat[x][0]] == "1.0"):
                if(givendat[x][len(givendat[0])-1] == "-1.0"):
                    falsepos += 1
                elif(givendat[x][len(givendat[0])-1] == "2.0"):
                    lowoccur += 1
                else:
                    truepos += 1
                    if givendat[x][0] not in picked:
                        picked.append(givendat[x][0])
            else:
                if(givendat[x][len(givendat[0])-1] == "1.0"):
                    falseneg += 1
                elif(givendat[x][len(givendat[0])-1] == "2.0"):
                    lowmiss += 1
                else:
                    trueneg += 1
    tot = len(dictofseqs)
    overallerror = (falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos)
    sens = truepos/(truepos+falseneg)
    spec = trueneg/(trueneg+falsepos)
    print("False Positives: " + str(falsepos))
    print("False Negatives: " + str(falseneg))
    print("True Positives: " + str(truepos))
    print("True Negatives: " + str(trueneg))
    print("CIMP-Low Occurrences: " + str(lowoccur))
    print("CIMP-Low Not Covered: " + str(lowmiss))
    print("Proportion of false positives: " + str((falsepos/tot)))
    print("Proportion of false negatives:" + str((falseneg/tot)))
    print("Accuracy: " + str((1-overallerror)))
    print("Error rate: " + str(overallerror))
    print("Sensitivity: " + str(sens))
    print("Specificity: " + str(spec))

def runGreedyOnTest(model, testdata):
    numrows = len(testdata)
    numcols = len(testdata[0])
    results = {}
    for x in range(0, numrows):
        for y in range(0, numcols-1): #program won't be able to see background/foreground
            if (testdata[x][y] == "1.0"):
                if (testdata[0][y] in model):
                    results[testdata[x][0]] = "1.0"

    for x in range(0,numrows):
        if(testdata[x][0] not in results):
            results[testdata[x][0]] = "-1.0"
    return results



if(len(sys.argv) > 1):
    datset = sys.argv[1]
else:
    #datset = input("What is the name of the dataset (looks at ../featurefilter)?: ")
    datset = "../../coadreadDATb4.csv"
with open("../../coadreadDATcomb.csv",'r') as f:
    it = csv.reader(f)
    listit = list(it)


perc = 0 #store the percent of foreground covered
lenseq = len(listit)
seqnames = []
F = []
infoF = []
SH = []
SN = []
negsamps = {}
possamps = {}
#get the negative and positive samples
for x in range(1,lenseq):
    for y in range(0, len(listit[x])-1):
        if y == 0:
            seqnames.append(listit[x][y])
        if(listit[0][y] == ''):
            continue
        #initialize pos and neg
        if listit[0][y] not in possamps:
            possamps[listit[0][y]] = list()
        if listit[0][y] not in negsamps:
            negsamps[listit[0][y]] = list()
        if listit[x][y] == "1.0":
            if listit[x][len(listit[0])-1] == "1.0":
                possamps[listit[0][y]].append(listit[x][0])
            elif listit[x][len(listit[0])-1] == "-1.0":
                negsamps[listit[0][y]].append(listit[x][0])


while(True):
    maxscore = -sys.maxsize - 1
    sel = ""
    posexists = False
    #for each mutation, calculate a score
    for mut in possamps:
        if len(possamps[mut]) > 1:
            posexists = True #there still exist features which can bring in pos
        evaltot = (len(possamps[mut]) - len(negsamps[mut]))
        if evaltot > maxscore and len(possamps[mut]) > 1:
            maxscore = evaltot
            sel = mut
    if posexists == False:
        print("hello!",maxscore)
        break

    #calculate new percent covered
    count = len(possamps[sel])
    print(sel + " " + "max score: " + str(maxscore))
    print("CIMP-H covered: " + str(count))
    perc += float(count/32) #add to percent covered
    myTup = (sel,perc)
    infoF.append(myTup)
    F.append(sel)
    for samp in possamps[sel]:
        SH.append(samp)
    for samp in negsamps[sel]:
        SN.append(samp)
    #print selected sequences (SF)
    #print(store[sel])
    posnew = {} #sequentially copy the new values into here
    negnew = {}
    for delseqs in possamps:
        if delseqs not in posnew:
            posnew[delseqs] = list()
            posnew[delseqs] = [y if y not in possamps[sel] else None for y in possamps[delseqs]]
            posnew[delseqs] = list(filter((None).__ne__, posnew[delseqs]))
    possamps = posnew
    possamps.pop(sel, None)
    for delseqs in negsamps:
        if delseqs not in negnew:
            negnew[delseqs] = list()
            negnew[delseqs] = [y if y not in negsamps[sel] else None for y in negsamps[delseqs]]
            negnew[delseqs] = list(filter((None).__ne__, negnew[delseqs]))


foreback = {}
#get pos/neg of samples for data purposes
for x in range(1,lenseq):
    if(listit[x][0] in SN or listit[x][0] in SH):
        foreback[listit[x][0]] = listit[x][len(listit[0])-1]

#F now contains the selected features
print(infoF)
print("-----------------------------------")
print(foreback)

picked = []
evalResults(runGreedyOnTest(F,listit),listit,picked)

for row in listit:
    if row[len(listit[0])-1] == "1.0" and row[0] not in picked:
        print(row[0])
