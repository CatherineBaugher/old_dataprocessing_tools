#-----------------------------------
#--  Data Mining Final Project    --
#--        Catherine Baugher      --
#--  Learning Ensemble Motifs     --
#-----------------------------------
#!/usr/bin/env python
import statistics
import os
import random as rn
import sys
import math
import copy
import csv

numTrees = 1000 #change value to change number of trees in the forest
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
def split(seqs, node, dat, mots,counter):
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
			if(float(dat[x][col]) == 0.0):
				lseqs.append(dat[x][0])
				lactual.append(dat[x][numcols-1])
			elif(float(dat[x][col]) == 1.0):
				rseqs.append(dat[x][0])
				ractual.append(dat[x][numcols-1])
	node.left = Tree()
	node.right = Tree()
	#if set of items is len 1, that means there's only one value for all:
	#meaning we can end as a leaf node
	if(len(set(lactual)) == 1):
		node.left.data = lactual[0]
	else:
		findoptimal(lseqs,node.left,dat,mots,counter)
	if(len(set(ractual)) == 1):
		node.right.data = ractual[0]
	else:
		findoptimal(rseqs,node.right,dat,mots,counter)

#findoptimal: uses phi to calculate the best motif to split at
#             input is the list of seqs
def findoptimal(seqs, node, dat, mots,counter):
	numcols = len(dat[0])
	numrows = len(dat)
	motscores = {}
	#for each motif, calculate phi for split candidate
	for x in range (1,numcols-1):
		numleft = numright = lback = rback = lfor = rfor = 0
		for y in range(1,numrows):
			if(dat[y][0] in seqs):
				if(float(dat[y][x]) == 0.0):
					numleft += 1
					if(float(dat[y][numcols-1]) == -1.0):
						lback += 1
					elif(float(dat[y][numcols-1]) == 1.0):
						lfor += 1
				elif(float(dat[y][x]) == 1.0):
					numright += 1
					if(float(dat[y][numcols-1]) == -1.0):
						rback += 1
					elif(float(dat[y][numcols-1]) == 1.0):
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
		if(selectedmotif not in counter):
			counter[selectedmotif] = 1
		else:
			counter[selectedmotif] += 1
		split(seqs,node,dat,mots,counter)

def genTree(dat,counter):
	numrows = len(dat)
	numcols = len(dat[0])
	mots = {}
	seqs = [] #seqs put in list to be divided down
	decTree = Tree()

	for x in range (1, numrows):
		seqs.append(dat[x][0])
	for y in range (1, numcols-1):
		mots[dat[0][y]] = y
		#print("dat[0][y] = " + dat[0][y])

	#run initial values. it will recurse to complete the tree
	findoptimal(seqs,decTree,dat,mots,counter)
	return decTree

def treePredictSeq(seq,model,testdata):
	try:
		if (float(model.data) == -1.0):
			return -1.0
		elif (float(model.data) == 1.0):
			return 1.0
	except(ValueError):
		for x in range(1, len(testdata)):
			if (testdata[x][0] == seq):
				motifind = testdata[0].index(model.data)
				nextrout = testdata[x][motifind]
				if(float(nextrout) == 1.0):
					return treePredictSeq(seq,model.right,testdata)
				else:
					return treePredictSeq(seq,model.left,testdata)

def evaluateForest(testingset,forest):
	answers = {}
	for x in range(1,len(testingset)):
		seq = testingset[x][0]
		votes = []
		for x in range(0,numTrees): #vote!
			votes.append(treePredictSeq(seq,forest[x],testingset))
		answers[seq] = (statistics.mode(votes),forest)
	return answers

def evalResults(dictofseqs,givendat,store_tp_samp,store_fn_samp,numb):
	falsepos = falseneg = truepos = trueneg = 0
	for x in range (1,len(givendat)):
		if(givendat[x][0] in dictofseqs):
			if(dictofseqs[givendat[x][0]][0] != float(givendat[x][len(givendat[0])-1])):
				if(float(dictofseqs[givendat[x][0]][0]) == 1.0):
					falsepos += 1
				else:
					falseneg += 1
					if givendat[x][0] in store_tp_samp:
						store_fn_samp[givendat[x][0]] += 1
					else:
						store_fn_samp[givendat[x][0]] = 1
			else:
				if(float(dictofseqs[givendat[x][0]][0]) == 1.0):
					truepos += 1
					if givendat[x][0] in store_tp_samp:
						store_tp_samp[givendat[x][0]] += 1
					else:
						store_tp_samp[givendat[x][0]] = 1
					trueposfeats.write("Features occuring in sample " + givendat[x][0] +"\n")
					trueposfeats.write("---------------------------------------------------------\n")
					#print trees of winning forest...
					storedfeats = {}
					winningforst = dictofseqs[givendat[x][0]][1]
					for treelet in winningforst:
						printTree(treelet,True,storedfeats) #get which features caused it

					for k, v in sorted(storedfeats.items(), key=lambda j:(-j[1],j[0])):
						trueposfeats.write(str(k)+" : "+str(v) + "\n")
					trueposfeats.write("\n\n\n")
				else:
					trueneg += 1
	tot = len(dictofseqs)
	overallerror = (falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos)
	sens = truepos/(truepos+falseneg)
	spec = trueneg/(trueneg+falsepos)
	numb = str(numb)
	print("[" + numb + "]" + "False Positives: " + str(falsepos))
	print("[" + numb + "]" + "False Negatives: " + str(falseneg))
	print("[" + numb + "]" + "True Positives: " + str(truepos))
	print("[" + numb + "]" + "True Negatives: " + str(trueneg))
	print("[" + numb + "]" + "Proportion of false positives: " + str((falsepos/tot)))
	print("[" + numb + "]" + "Proportion of false negatives:" + str((falseneg/tot)))
	print("[" + numb + "]" + "Accuracy: " + str((1-overallerror)))
	treeinfo.write("ACCURACY OF FOLD: " + str((1-overallerror)) + "\n")
	print("[" + numb + "]" + "Error rate: " + str(overallerror))
	print("[" + numb + "]" + "Sensitivity: " + str(sens))
	print("[" + numb + "]" + "Specificity: " + str(spec))

#getPartitions: given as input an integer, being the size of the data
#               output is a list of tuples for the indices of the test data
def getPartitions(size):
	listofindices = []
	for x in range(0,10):
		listofindices.append(((size/10)*x,(size/10)*(x+1)))
	return listofindices

#RANDOM FOREST
if(len(sys.argv) > 1):
	datset = sys.argv[1]
else:
	datset = input("What is the name of the dataset (looks at ../featurefilter)?: ")
#path = "/fs/project/PHS0293/cancerproj/cimp-noncimp/featurefilter/" + datset + ".csv"
path = "../../featurefilter/" + datset + ".csv"
with open(path,'r') as f:
	it = csv.reader(f)
	listit = list(it)

#stores the data we are gathering... reduce redundancies
#resultsfilepath = "/fs/project/PHS0293/cancerproj/cimp-noncimp/assessdata/frequent_features/" + datset + "_FEATUREINFO" + ".txt"
#resultsfilepath = "../assessdata/frequent_features/" + datset + "_FEATUREINFO" + ".txt"
#results = open(resultsfilepath,"r") #open for read at first
#load up current information so we don't cause redundancies
linect = 0
numpastruns = 0
counter = {}
#if(os.stat(resultsfilepath).st_size > 0):
#	for line in results:
#		line = line.rstrip()
#		if(linect == 0):
#			numpastruns = int(line)
#		else:
#			explodedfeat = line.split(" = ") #split line into 2: feature and num occurence
#			counter[explodedfeat[0]] = int(explodedfeat[1])
#		linect += 1

#results.close()
#results = open(resultsfilepath,"w") #now open for w, as r+ will append...


store_tp_samp = {}
store_fn_samp = {}
#sampstruepos = open("/fs/project/PHS0293/cancerproj/cimp-noncimp/randomforest/truepossamples.txt","w")
#trueposfeats = open("/fs/project/PHS0293/cancerproj/cimp-noncimp/randomforest/features_truepos","w")
#sampsfalseneg = open("/fs/project/PHS0293/cancerproj/cimp-noncimp/randomforest/falsenegsamples.txt","w")
sampstruepos = open("./truepossamples.txt","w")
trueposfeats = open("./features_truepos","w")
sampsfalseneg = open("./falsenegsamples.txt","w")

#The files below are for testing the random feature selection
#BEFORE BUILDING TREE
rowsbefore = open("./rowsselected","w")
featsbefore = open("./featsselected","w")
#AFTER BUILDING TREE
treeinfo = open("./treeinfo","w")

#shuffle the data
shuffledbottom = listit[1:]
rn.shuffle(shuffledbottom)
listit = [listit[0]] + shuffledbottom

#separate datafile into foreground and background
#NO LABELS
foreground = []
background = []
numcols = len(listit[0])
for x in range(1,len(listit)):
	if (listit[x][numcols-1] == "-1.0"):
		background.append(listit[x])
	elif (listit[x][numcols-1] == "1.0"):
		foreground.append(listit[x])

for numb in range(10):
	forest = []

	#start writing to testing files
	rowsbefore.write("Fold #" + str(numb+1) + "\n------------------\n")
	featsbefore.write("Fold #" + str(numb+1) + "\n------------------\n")
	treeinfo.write("Fold #" + str(numb+1) + "\n------------------\n")
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
			if(x >= testforeparts[numb][0] and x < testforeparts[numb][1]):
				testdat.append(foreground[x])
			else:
				traindat.append(foreground[x])
		if(x < bglen):
			if(x >= testbackparts[numb][0]  and  x < testbackparts[numb][1]):
				testdat.append(background[x])
			else:
				traindat.append(background[x])

	#train the model
	#first bag up the samples
	for x in range(0,numTrees): #this is number of trees and can be changed
		bagsample = []
		#write which tree we're on
		featsbefore.write("TREE " + str(x+1) + ":\n")
		rowsbefore.write("TREE " + str(x+1) + ":\n")
		treeinfo.write("TREE " + str(x+1) + ":\n")
		for z in range(0,len(traindat)): #doing bootstrap samples of size n
			bagsample.append(traindat[rn.randrange(1,len(traindat))])
		#write to test file
		for z in range(0,len(bagsample)):
			for a in range(0,len(bagsample[0])):
				rowsbefore.write(str(bagsample[z][a]) + ",")
			rowsbefore.write("\n")
		rowsbefore.write("\n")

		newset = [[] for i in range (len(traindat))]
		#append sample names
		for z in range(0,len(traindat)):
			newset[z].append(traindat[z][0])
		#take sqrt of total features in bootstrap aggregation
		#featamount = int(math.sqrt(len(traindat[0])-2))
		featamount = 6
		#print("D size: " + str(len(traindat[0])-2))
		#print("d size: " + str(featamount))
		uniquefeats = []
		for y in range(0,featamount): #rand select features of size sqrt(x) where x = num features. not allowing repeats.
			col = rn.randrange(1,len(traindat[0])-1)
			while(col in uniquefeats):
				col = rn.randrange(1,len(traindat[0])-1)
			uniquefeats.append(col)
			for z in range(0,len(traindat)):
				newset[z].append(traindat[z][col])
		featsbefore.write("\n")
		#print("double checking d size: " + str(len(newset[0])-1))
		#append class
		for z in range(0,len(traindat)):
			newset[z].append(traindat[z][len(traindat[0])-1])
		bagsample = copy.deepcopy(newset)
		#using new sample, generate tree
		ourtree = genTree(bagsample,counter)
		forest.append(ourtree)
		#print out tree
		usedfeats = {}
		dep = printTree(ourtree,True,usedfeats)
		for k, v in sorted(usedfeats.items(), key=lambda x:(-x[1],x[0])):
			treeinfo.write(str(k)+" : "+str(v) + "\n")
		treeinfo.write("---\n")
		treeinfo.write("DEPTH OF TREE: " + str(dep) + "\n\n")
		
		

	#space out the folds...
	featsbefore.write("\n\n")
	rowsbefore.write("\n\n")
	
	#test the model
	dictofseqs = evaluateForest(testdat,forest)
	evalResults(dictofseqs,testdat,store_tp_samp,store_fn_samp,numb)

	treeinfo.write("\n\n")
	print("\n")

for k,v in sorted(counter.items(),key=lambda x:(-x[1],x[0])):
	print(k,":",v)
'''
#write out stored data about runs
#results.write(str(numpastruns + 1) + "\n")
#for k, v in sorted(counter.items(), key=lambda x:(-x[1],x[0])):
#	results.write(str(k)+" = "+str(v) + "\n")
#
for k, v in sorted(store_tp_samp.items(), key=lambda x:(-x[1],x[0])):
	sampstruepos.write(str(k)+" : "+str(v) + "\n")

for k, v in sorted(store_fn_samp.items(), key=lambda x:(-x[1],x[0])):
	sampsfalseneg.write(str(k)+" : "+str(v) + "\n")
'''
