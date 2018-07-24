# CALCCIMP_ALL.PY
# finds number of CIMP+ and CIMP-
# across all features
#!/usr/bin/env python

import csv
from operator import itemgetter

inpdat = "../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)

scores = {} #dict of strings->tuples (cimp+,cimp-)
endcol = len(listit[0])-1
endrow = len(listit)

for y in range(1,endcol): #for each mut, minus class
	cimppos = cimpneg = 0
	for x in range(1,endrow): #for each sample...
		if(float(listit[x][y]) == 1.0): #we have a hit...
			if(float(listit[x][endcol]) == 1.0):
				cimppos += 1
			elif(float(listit[x][endcol]) == -1.0):
				cimpneg += 1
	scores[listit[0][y]] = (cimppos,cimpneg)

#write out results sorted by positive
results = open("./cimpcount_all_sortPOS.txt","w")
results.write("SORTED BY CIMP COUNT DESCENDING\n")
results.write("format: featurename = (CIMP+,CIMP-)\n")
results.write("-------------------------------------------\n")
for key,value in sorted(scores.items(), key=itemgetter(1), reverse=True):
	results.write(str(key)+" = "+str(value)+"\n")

results.close()

#write out results sorted by negative
results = open("./cimpcount_all_sortNEG.txt","w")
results.write("SORTED BY NON-CIMP COUNT DESCENDING\n")
results.write("format: featurename = (CIMP+,CIMP-)\n")
results.write("-------------------------------------------\n")
for key,value in sorted(scores.items(), key=lambda t:t[1][1], reverse=True):
	results.write(str(key)+" = "+str(value)+"\n")
