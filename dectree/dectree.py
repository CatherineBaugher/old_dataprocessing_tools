#!/usr/bin/env python
import statistics
import os
import random as rn
import sys
import math
import copy
import csv

class Tree(object):
	def __init__(self):
		self.left = None
		self.right = None
		self.data = None

	def __str__(self):
		return str(self.data)

#printTree: used to print the fully generated tree.
#           gives the selected motifs
def printTree(root,flag=False,feats={},dep=0):
        #prints breadth first, level by level
	curr = [root]
	while curr:
		dep += 1
		if(not flag):
			print(' '.join(str(node) for node in curr))
			print('\n')
		else:
			for node in curr:
				try: #see if we are looking at a classification or feature
					check = float(node)
				except: #means it was a string = a feature, not classification
					if str(node) != "1.0" and str(node) != "-1.0":
						if str(node) not in feats:
							feats[str(node)] = 1
						else:
							feats[str(node)] += 1
		next = list()
		for node in curr:
			if node.left:
				next.append(node.left)
			if node.right:
				next.append(node.right)
			curr = next
	return dep


def findMaj(seqs,dat):
	numBack = numFore = 0
	numcols = len(dat[0])
	numrows = len(dat)
	for x in range (1, numrows):
		if(dat[x][0] in seqs):
			if(float(dat[x][numcols-1]) == -1.0):
				numBack += 1
			elif(float(dat[x][numcols-1]) == 1.0):
				numFore += 1

	if(numBack >= numFore):
		return -1.0
	else:
		return 1.0

#split: creates the recursive split of the tree.
#       input is a node w/ motif name, recursively calls findoptimal
def split(seqs, node, dat, mots,freqfeats):
	#when called, node should already contain data = motif name
	col = mots[node.data]
	numrows = len(dat)
	numcols = len(dat[0])
	#create lists to store both the seqs splitting to each side
	#as well as actual classes, so we can determine when to stop recursing
	lseqs = []
	rseqs = []
	lactual = []
	ractual = []
	#split across left and right
	for x in range (1, numrows):
		if(dat[x][0] in seqs):
			if(dat[x][col] == "0.0"):
				lseqs.append(dat[x][0])
				lactual.append(dat[x][numcols-1])
			elif(dat[x][col] == "1.0"):
				rseqs.append(dat[x][0])
				ractual.append(dat[x][numcols-1])
	node.left = Tree()
	node.right = Tree()
	#if set of items is len 1, that means there's only one value for all:
	#meaning we can end as a leaf node
	if(len(set(lactual)) == 1):
		node.left.data = lactual[0]
	else:
		findoptimal(lseqs,node.left,dat,mots,freqfeats)
	if(len(set(ractual)) == 1):
		node.right.data = ractual[0]
	else:
		findoptimal(rseqs,node.right,dat,mots,freqfeats)

#findoptimal: uses phi to calculate the best motif to split at
#             input is the list of seqs
def findoptimal(seqs, node, dat, mots,freqfeats):
	numcols = len(dat[0])
	numrows = len(dat)
	motscores = {}
	#for each motif, calculate phi for split candidate
	for x in range (1,numcols-1):
		numleft = numright = lback = rback = lfor = rfor = 0
		for y in range(1,numrows):
			if(dat[y][0] in seqs):
				if(dat[y][x] == "0.0"):
					numleft += 1
					if(dat[y][numcols-1] == "-1.0"):
						lback += 1
					elif(dat[y][numcols-1] == "1.0"):
						lfor += 1
				elif(dat[y][x] == "1.0"):
					numright += 1
					if(dat[y][numcols-1] == "-1.0"):
						rback += 1
					elif(dat[y][numcols-1] == "1.0"):
						rfor += 1
		PL = numleft/(numrows-1)
		PR = numright/(numrows-1)
		T = len(seqs)
		Qfor = abs((lfor / T) - (rfor / T))
		Qbac = abs((lback / T) - (rback / T))
		phi = 2 * PL * PR * (Qfor + Qbac)
		motscores[dat[0][x]] = phi

	#next, find max phi out of motifs
	selectedmotif = max(motscores, key=motscores.get)
	bestscore = motscores[selectedmotif]
	if(bestscore == 0.0):
		#this is an additional base case I found.
		#if there is not an optimal motif, look at results and pick majority
		node.data = findMaj(seqs,dat)
		return
	else:
		node.data = selectedmotif
		if(selectedmotif not in freqfeats):
			freqfeats[selectedmotif] = 0
		freqfeats[selectedmotif] += 1
		split(seqs,node,dat,mots,freqfeats)

def decisionTree(listit,freqfeats):
	numrows = len(listit)
	numcols = len(listit[0])
	mots = {}
	seqs = [] #seqs put in list to be divided down
	decTree = Tree()

	for x in range (1, numrows):
		seqs.append(listit[x][0])
	for y in range (1, numcols-1):
		mots[listit[0][y]] = y

	#run initial values. it will recurse to complete the tree
	findoptimal(seqs,decTree,listit,mots,freqfeats)
	return decTree
#TESTING FNS BELOW
#------------------------------

#getPartitions: given as input an integer, being the size of the data
#               output is a list of tuples for the indices of the test data
def getPartitions(size):
	listofindices = []
	for x in range(0,10):
		listofindices.append(((size/10)*x,(size/10)*(x+1)))
	return listofindices

#treePredictSeq: predict whether a sequence is foreground or background
#                just descend recursively. the base case is a leaf node, -1 or 1
def treePredictSeq(seq,model,testdata):
	if (str(model.data) == "-1.0"):
		return "-1.0"
	elif (str(model.data) == "1.0"):
		return "1.0"
	else:
		for x in range(0, len(testdata)):
			if (testdata[x][0] == seq):
				motifind = testdata[0].index(model.data)
				nextrout = testdata[x][motifind]
				if(nextrout == "1.0"):
					return treePredictSeq(seq,model.right,testdata)
				else:
					return treePredictSeq(seq,model.left,testdata)


def runDecTreeOnTest(model, testdata):
	results = {}
	for x in range(1,len(testdat)):
		newval = treePredictSeq(testdat[x][0],model,testdata)
		if(newval == "1.0"): 
			results[testdat[x][0]] = "1.0"
		else:
			results[testdat[x][0]] = "-1.0"

	return results

def evalResults(dictofseqs,givendat,i):
	falsepos = falseneg = truepos = trueneg = 0
	for x in range (1,len(givendat)):
		if(givendat[x][0] in dictofseqs):
			if(dictofseqs[givendat[x][0]] != givendat[x][len(givendat[0])-1]):
				if(dictofseqs[givendat[x][0]] == "1.0"):
					falsepos += 1
				else:
					falseneg += 1
			else:
				if(dictofseqs[givendat[x][0]] == "1.0"):
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


if(len(sys.argv) > 1):
	datset = sys.argv[1]
else:
	datset = input("What is the name of the dataset (looks at ../featurefilter)?: ")
#path = "/fs/project/PHS0293/cancerproj/cimp-noncimp/featurefilter/" + datset + ".csv"
path = "../featurefilter/" + datset + ".csv"
with open(path,'r') as f:
	it = csv.reader(f)
	listit = list(it)

#separate datafile into foreground and background
#NO LABELS
foreground = []
background = []
numcols = len(listit[0])
#NOTE TO SELF: NEED TO FIX BELOW
for x in range(1,len(listit)):
	if (x != 0):
		if (listit[x][numcols-1] == "-1.0"):
			background.append(listit[x])
		elif (listit[x][numcols-1] == "1.0"):
			foreground.append(listit[x])

counter = {}
#run k=3 fold
for k in range(10):
	#the data of both sets starts out w motifs at top
	testdat = [listit[0]]
	traindat = [listit[0]]
	fglen = len(foreground)
	bglen = len(background)
	testforeparts = getPartitions(fglen)
	testbackparts = getPartitions(bglen)
	#print("foreground: " + ', '.join(str(d) for d in testforeparts))
	#print("background: " + ', '.join(str(d) for d in testbackparts))

	for x in range (0, (max(fglen,bglen))):
		if(x < fglen):
			if(x >= testforeparts[k][0] and x <= testforeparts[k][1]):
				testdat.append(foreground[x])
			else:
				traindat.append(foreground[x])
		if(x < bglen):
			if(x >= testbackparts[k][0]  and  x <= testbackparts[k][1]):
				testdat.append(background[x])
			else:
				traindat.append(background[x])

	myDecTree = decisionTree(traindat,counter)

	decResults = runDecTreeOnTest(myDecTree, testdat)

	evalResults(decResults,testdat,(k+1))
	print("\n")

for k,v in sorted(counter.items(),key=lambda x:(-x[1],x[0])):
	print(k,":",v)
	print("\n\n")

