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

accpath = "filtered_accuracy005.csv"
infpath = "filtered_infogain005.csv"

with open(accpath,'r') as f:
	it = csv.reader(f)
	accdat = list(it)

with open(infpath,'r') as f:
	it = csv.reader(f)
	infdat = list(it)

accmuts = list(accdat[0][:-1])
infmuts = list(infdat[0][:-1])
print("cols in infogain:",len(infmuts))
print("cols in accuracy:",len(accmuts))
newset = []
lastcol = []

#doesn't matter which set the classifications come from
for row in accdat: #because they're both the same
	lastcol.append(row[len(accdat[0])-1])

rows = len(accdat)
end = len(accdat[0])-1
for row in infdat:
	newset.append(row[:-1])

appendcol = []
currmuts = list(newset[0])
for x in range(1,end):
	if(accmuts[x] not in currmuts):
		appendcol.append(x)
		currmuts.append(accdat[0][x])

for ind in appendcol:
	for x in range(0,rows):
		newset[x].append(accdat[x][ind])

#lastly attach the classifications...
for x in range(0,rows):
	newset[x].append(lastcol[x])

with open("union_acc005inf005.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newset)


print("cols in newset:",len(newset[0]))
