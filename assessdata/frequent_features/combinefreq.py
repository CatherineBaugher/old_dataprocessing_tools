# COMBINEFREQ.PY
# Combines freq features across all "_FEATUREINFO" files
# this data can then be used to find accuracy, info gain, CIMP+/CIMP-
#!/usr/bin/env python

import csv
import os

acc05 = open("./filtered_accuracy05_FEATUREINFO.txt","r")
inf05 = open("./filtered_infogain05_FEATUREINFO.txt","r")
union05 = open("./union_acc05inf05_FEATUREINFO.txt","r")

results = open("./FEATUREINFO_combined.txt","w")

counter = {}
linect = 0
if(os.stat("./filtered_accuracy05_FEATUREINFO.txt").st_size > 0):
	for line in acc05:
		line = line.rstrip()
		if(linect != 0): #skip num runs
			explodedfeat = line.split(" = ") #split line into 2: feature and num occurence
			counter[explodedfeat[0]] = int(explodedfeat[1])
		linect += 1

linect = 0
if(os.stat("./filtered_infogain05_FEATUREINFO.txt").st_size > 0):
	for line in inf05:
		line = line.rstrip()
		if(linect != 0): #skip num runs
			explodedfeat = line.split(" = ") #split line into 2: feature and num occurence
			if(explodedfeat[0] not in counter):
				counter[explodedfeat[0]] = int(explodedfeat[1])
			else:
				counter[explodedfeat[0]] += int(explodedfeat[1])
		linect += 1

linect = 0
if(os.stat("./union_acc05inf05_FEATUREINFO.txt").st_size > 0):
	for line in union05:
		line = line.rstrip()
		if(linect != 0): #skip num runs
			explodedfeat = line.split(" = ") #split line into 2: feature and num occurence
			if(explodedfeat[0] not in counter):
				counter[explodedfeat[0]] = int(explodedfeat[1])
			else:
				counter[explodedfeat[0]] += int(explodedfeat[1])
		linect += 1


#write stored count into results
for k, v in sorted(counter.items(), key=lambda x:(-x[1],x[0])):
	results.write(str(k)+" = "+str(v) + "\n")
