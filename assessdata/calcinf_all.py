# -----------------------------------------------------------------------------$
# filtinfogain05.py
# result is new dataset with only features in top .05% info gain
# info gain(S,mutation) = E(S) - E(S,mutation)
# our target (S) is CIMP classification
# in short, calculate entropy of stump, then subtract the entropy of "decisions"
# -----------------------------------------------------------------------------$
import os
import csv
import math
import statistics

inpdat = "../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)

print("col # of old:",len(listit[0]))

#first find entropy of S
fore = back = 0
tot = len(listit) - 1
endcol = len(listit[0]) - 1
for x in range(1,len(listit)): #take a look at each row
	if float(listit[x][endcol]) == -1.0: #found background
		back += 1
	elif float(listit[x][endcol]) == 1.0: #found foreground
		fore += 1
entS = -fore/tot * math.log((fore/tot),2) - back/tot * math.log((back/tot),2)

scores = {}
#now find the entropy of each mut, then determine info gain
for y in range(1,endcol): #for each mut, minus class
	Rpos = Rneg = Rtot = Lpos = Lneg = Ltot = 0
	for x in range(1,len(listit)): #look at each sample
		if(float(listit[x][y]) == 1.0): #if mutation present...
			if(float(listit[x][endcol]) == 1.0):
					Rpos += 1
			if(float(listit[x][endcol]) == -1.0):
					Rneg += 1
			Rtot += 1
		elif(float(listit[x][y]) == 0.0): #if mutation not present...
			if(float(listit[x][endcol]) == 1.0):
					Lpos += 1
			if(float(listit[x][endcol]) == -1.0):
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
	scores[y] = entS - (Rtot/tot)*entR - (Ltot/tot)*entL

#now come up with stats
avg = statistics.mean(scores.values())
med = statistics.median(scores.values())
min = min(scores.values())
max = max(scores.values())
range = max - min
stddev = statistics.stdev(scores.values())

results = open("./infstats_all.txt","w")
results.write("Stats of info gain across all features\n")
results.write("------------------------------------------------\n\n")
results.write("Average: "+str(avg)+"\n")
results.write("Median: "+str(med)+"\n")
results.write("Minimum: "+str(min)+"\n")
results.write("Maximum: "+str(max)+"\n")
results.write("Range: "+str(range)+"\n")
results.write("Standard dev: "+str(stddev)+"\n")
