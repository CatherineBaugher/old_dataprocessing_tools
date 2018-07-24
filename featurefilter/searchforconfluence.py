# -----------------------------------------------------------------------------$
# filtinfogain1.py
# result is new dataset with only features in top 1% info gain
# info gain(S,mutation) = E(S) - E(S,mutation)
# our target (S) is CIMP classification
# in short, calculate entropy of stump, then subtract the entropy of "decisions"
# -----------------------------------------------------------------------------$
import os
import csv
import math

accpath = "filtered_accuracy0025.csv"
infpath = "filtered_infogain0025.csv"

with open(accpath,'r') as f:
	it = csv.reader(f)
	accdat = list(it)

with open(infpath,'r') as f:
	it = csv.reader(f)
	infdat = list(it)

keep = [0] #need to keep samples

accmuts = list(accdat[0][:-1])
infmuts = list(infdat[0][:-1])
print("cols in infogain:",len(infmuts))
print("cols in accuracy:",len(accmuts))
newset = []
lastcol = []
conf = open("confluence0025.txt","w")
#doesn't matter which set the classifications come from
for row in accdat: #because they're both the same
	lastcol.append(row[len(accdat[0])-1])

lesserlen = "accmuts"
for row in infdat:
	newset.append(row[:-1])

appendcol = []
currmuts = list(newset[0])
for x in range(1,len(accdat[0])-1):
	if(accdat[0][x] in infdat[0]):
		keep.append(x)
		conf.write(accdat[0][x] + "\n")

keep.append(len(infdat[0])-1) #need to also keep the classifications

newdatset = [[row[c] for c in keep] for row in accdat]


with open("confluence0025.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newdatset)
