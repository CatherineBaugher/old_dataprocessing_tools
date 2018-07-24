# CALCCIMP_FREQ.PY
# finds number of CIMP+ and CIMP-
# across features that appear in random forest
#!/usr/bin/env python

import csv
from operator import itemgetter

inpdat = open("./FEATUREINFO_combined.txt","r")
with open("../../../coadreadDAT.csv","r") as f:
	it = csv.reader(f)
	checkdat = list(it)

results = open("./cimpcount_freqfeats.txt","w")
results.write("SORTED BY OCCURENCE IN RANDOM FOREST\n")
results.write("format: featurename = (CIMP+,CIMP-)\n")
results.write("-------------------------------------------\n")

scores = {} #dict of strings->tuples (cimp+,cimp-)
endcol = len(checkdat[0])-1
endrow = len(checkdat)
for line in inpdat:
	line = line.rstrip()
	explodedfeat = line.split(" = ") #split line into 2: feature and num occurence. only need first one.
	y = checkdat[0].index(explodedfeat[0]) #find index in coadreadDAT
	cimppos = cimpneg = 0
	for x in range(1,endrow): #for each sample...
		if(float(checkdat[x][y]) == 1.0): #we have a hit...
			if(float(checkdat[x][endcol]) == 1.0):
				cimppos += 1
			elif(float(checkdat[x][endcol]) == -1.0):
				cimpneg += 1
	val = (cimppos,cimpneg)
	scores[explodedfeat[0]] = val
	results.write(explodedfeat[0] + " = " + str(val) + "\n")


#scores dict can be used later to sort by cimp+ or cimp-
#for now, it just prints by occurence in random forest
