# CALCCIMP_FREQ.PY
# finds number of CIMP+ and CIMP-
# across features that appear in random forest
#!/usr/bin/env python

import csv
from operator import itemgetter
import os
import math
import statistics

inpdat = open("./FEATUREINFO_combined.txt","r")
with open("../../../coadreadDAT.csv","r") as f:
	it = csv.reader(f)
	checkdat = list(it)

results = open("./infogain_freqfeats.txt","w")

scores = {} #dict of strings->tuples (cimp+,cimp-)
endcol = len(checkdat[0])-1
endrow = len(checkdat)

#first find entropy of S
fore = back = 0
tot = len(checkdat) - 1
endcol = len(checkdat[0]) - 1
for x in range(1,len(checkdat)): #take a look at each row
	if float(checkdat[x][endcol]) == -1.0: #found background
		back += 1
	elif float(checkdat[x][endcol]) == 1.0: #found foreground
		fore += 1
entS = -fore/tot * math.log((fore/tot),2) - back/tot * math.log((back/tot),2)

scores = {}

#next calc entropy for each feature and find info gain
for line in inpdat:
	line = line.rstrip()
	explodedfeat = line.split(" = ") #split line into 2: feature and num occurence. only need first one.
	y = checkdat[0].index(explodedfeat[0]) #find index in coadreadDAT

	Rpos = Rneg = Rtot = Lpos = Lneg = Ltot = 0
	for x in range(1,len(checkdat)): #look at each sample
		if(float(checkdat[x][y]) == 1.0): #if mutation present...
			if(float(checkdat[x][endcol]) == 1.0):
					Rpos += 1
			if(float(checkdat[x][endcol]) == -1.0):
					Rneg += 1
			Rtot += 1
		elif(float(checkdat[x][y]) == 0.0): #if mutation not present...
			if(float(checkdat[x][endcol]) == 1.0):
					Lpos += 1
			if(float(checkdat[x][endcol]) == -1.0):
					Lneg += 1
			Ltot += 1
	if(Rpos == 0 or Rneg == 0):
		entR = 0
	else:
		entR = -Rpos/Rtot * math.log((Rpos/Rtot),2) - Rneg/Rtot * math.log((Rneg/Rtot),2)
	if(Lpos == 0 or Lneg == 0):
		entL = 0
	else:
		entL = -Lpos/Ltot * math.log((Lpos/Ltot),2) - Lneg/Ltot * math.log((Lneg/Ltot),2)
	infg = entS - (Rtot/tot)*entR - (Ltot/tot)*entL
	scores[y] = infg
	results.write(explodedfeat[0] + " = " + str(infg) + "\n")


#now come up with stats
avg = statistics.mean(scores.values())
med = statistics.median(scores.values())
min = min(scores.values())
max = max(scores.values())
range = max - min
stddev = statistics.stdev(scores.values())

results.write("\n\n\nStats of info gain across all features\n")
results.write("------------------------------------------------\n\n")
results.write("Average: "+str(avg)+"\n")
results.write("Median: "+str(med)+"\n")
results.write("Minimum: "+str(min)+"\n")
results.write("Maximum: "+str(max)+"\n")
results.write("Range: "+str(range)+"\n")
results.write("Standard dev: "+str(stddev)+"\n")

