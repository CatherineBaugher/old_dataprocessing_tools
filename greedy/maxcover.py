#-----------------------------------
#--        Catherine Baugher      --
#--       Coverage Algorithm      --
#-----------------------------------
#!/usr/bin/env python
import csv
import operator
import pprint
import sys
from copy import copy
import random as rn
from sklearn.cross_validation import KFold

#GREEDY SELECTION FNS BELOW
#------------------------------
#evalResults: given a dictionary of seqs mapped to predictions
#             determine results of the evaluation (FN, TN, FP, TP, error, accuracy etc)
def evalResults(dictofseqs,givendat,i):
	falsepos = falseneg = truepos = trueneg = 0
	for x in range (1,len(givendat)):
		if(givendat[x][0] in dictofseqs):
			if(float(dictofseqs[givendat[x][0]]) != float(givendat[x][len(givendat[0])-1])):
				if(float(dictofseqs[givendat[x][0]]) == 1.0):
					falsepos += 1
				else:
					falseneg += 1
			else:
				if(float(dictofseqs[givendat[x][0]]) == 1.0):
					truepos += 1
				else:
					trueneg += 1
	tot = len(dictofseqs)
	overallerror = (falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos)
	sens = truepos/(truepos+falseneg)
	spec = trueneg/(trueneg+falsepos)
	k = str(i)
	print("[" + k + "]" + "False Positives: " + str(falsepos))
	print("[" + k + "]" + "False Negatives: " + str(falseneg))
	print("[" + k + "]" + "True Positives: " + str(truepos))
	print("[" + k + "]" + "True Negatives: " + str(trueneg))
	print("[" + k + "]" + "Proportion of false positives: " + str((falsepos/tot)))
	print("[" + k + "]" + "Proportion of false negatives:" + str((falseneg/tot)))
	print("[" + k + "]" + "Accuracy: " + str((1-overallerror)))
	print("[" + k + "]" + "Error rate: " + str(overallerror))
	print("[" + k + "]" + "Sensitivity: " + str(sens))
	print("[" + k + "]" + "Specificity: " + str(spec))

def runGreedyOnTest(model, testdata):
	numrows = len(testdata)
	numcols = len(testdata[0])
	results = {}
	for x in range(1, numrows):
		for y in range(1, numcols-1): #program won't be able to see background/foreground
			if (float(testdata[x][y]) == 1.0):
				if (testdata[0][y] in model):
					results[testdata[x][0]] = 1.0
	
	for x in range(1,numrows):
		if(testdata[x][0] not in results):
			results[testdata[x][0]] = -1.0
	return results

path = "../../3ormoreDATLOW.csv"
print("using file",path)
with open(path,'r') as f:
	it = csv.reader(f)
	listit = list(it)

#set number of folds
numfolds = 10

#split data from header
header = listit[0]
listit = listit[1:]

#shuffle the data
rn.shuffle(listit)

#find testing index
kf = KFold(len(listit),n_folds=numfolds,random_state=True)
indices = []
for trainind,testind in kf:
    indices.append(testind)

for i in range(numfolds):
	#make testing and training sets
	trainset = [header]
	testset = [header]
	for x in range(0,len(listit)):
		if(x in indices[i]):
			testset.append(listit[x])
		else:
			trainset.append(listit[x])

	#setup greedy algorithm
	delta = .05 #hardcode delta to be 5%. this can easily be changed to allow input
	lenseq = len(trainset)
	seqnames = []
	F = []
	infoF = []
	SF = []
	store = {}
	perc = 0
	for x in range(0,lenseq):
		for y in range(0, len(trainset[x])-1):
			if y == 0:
				seqnames.append(trainset[x][y])
			elif float(trainset[x][y]) == 1.0 and float(trainset[x][len(trainset[0])-1]) == 1.0:
				if trainset[0][y] not in store:
					store[trainset[0][y]] = list()
				store[trainset[0][y]].append(trainset[x][0])

	while(True):
		max = 0
		sel = ""
		count = 0
		for motif in store:
			#store[motif] = [x for x in store[motif] if x != '']
			if len(store[motif]) > max:
				max = len(store[motif])
				sel = motif
		if sel == "":
			break
		#calculate new percent
		for x in range(0,lenseq):
			if(trainset[x][0] in store[sel]):
				if(float(trainset[x][len(trainset[0])-1]) == 1.0): #positive
					count += 1
		#print("max: " + str(max))
		perc += float(count/32)
		myTup = (sel,perc)
		infoF.append(myTup)
		F.append(sel)
		for seq in store[sel]:
			SF.append(seq)
			
		#print selected sequences (SF)
		#print(store[sel])
		newguy = {} #sequentially copy the new values into here
		for delseqs in store:
			if delseqs not in newguy:
				newguy[delseqs] = list()
				newguy[delseqs] = [y if y not in store[sel] else None for y in store[delseqs]]
				newguy[delseqs] = list(filter((None).__ne__, newguy[delseqs]))
		store = newguy
		store.pop(sel, None)

	'''
	foreback = {}
	#get pos/neg of samples for data purposes
	for x in range(1,lenseq):
		if(trainset[x][0] in SF):
			foreback[trainset[x][0]] = trainset[x][len(trainset[0])-1]
	'''

	#F now contains the selected features
	print(infoF)
	print("-----------------------------------")
	#print(foreback)

	evalResults(runGreedyOnTest(F,testset),testset,0)
	print("-----------------------------------")
