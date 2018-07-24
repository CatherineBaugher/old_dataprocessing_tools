# CALCACC_ALL.PY
# Reports statistics of accuracies across
# across all features
#!/usr/bin/env python

import statistics
import csv
from operator import itemgetter

# CALCACC_FREQ.PY
# finds accuracies
# across features that appear in random forest
#!/usr/bin/env python

import csv
from operator import itemgetter

inpdat = open("./FEATUREINFO_combined.txt","r")
with open("../../../coadreadDAT.csv","r") as f:
	it = csv.reader(f)
	checkdat = list(it)

results = open("./accuracy_freqfeats.txt","w")
scores = {} #dict of strings->tuples (cimp+,cimp-)
endcol = len(checkdat[0])-1
endrow = len(checkdat)
for line in inpdat:
	line = line.rstrip()
	explodedfeat = line.split(" = ") #split line into 2: feature and num occurence. only need first one.
	y = checkdat[0].index(explodedfeat[0]) #find index in coadreadDAT

	falseneg = falsepos = trueneg = truepos = 0
	left = []
	right = []
	for x in range(1,endrow): #look at each sample
		if(float(checkdat[x][y]) == 1.0):
			right.append((checkdat[x][0],float(checkdat[x][endcol])))
		elif(float(checkdat[x][y]) == 0.0):
			left.append((checkdat[x][0],float(checkdat[x][endcol])))

	#now that we have a stump, analyze as we would a dead end in dec tree
	#mode rule: if there are equal occurances between -1 and 1, pick 1
	try:
		majl = statistics.mode(x[1] for x in left)
	except:
		majl = -1.0
	try:
		majr = statistics.mode(x[1] for x in right)
	except:
		majr = -1.0
	#now classify all samples under the majority...
	classif = {}
	for x in left:
		classif[x[0]] = majl
	for x in right:
		classif[x[0]] = majr
	#now score the results...
	for x in range(1,endrow):
		if(float(checkdat[x][endcol]) == 1.0):
			if(classif[checkdat[x][0]] == 1.0):
				truepos += 1
			elif(classif[checkdat[x][0]] == -1.0):
				falsepos += 1
			else:
				print("ERROR1")
		elif(float(checkdat[x][endcol]) == -1.0):
			if(classif[checkdat[x][0]] == 1.0):
				falseneg += 1
			elif(classif[checkdat[x][0]] == -1.0):
				trueneg += 1
			else:
				print("ERROR2")
		else:
			print(checkdat[x][endcol])
	#print(str(falseneg),str(falsepos),str(truepos),str(trueneg),"\n")
	accuracy = (falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos)
	scores[y] = accuracy
	results.write(explodedfeat[0] + " = " + str(accuracy) + "\n")

#now come up with stats
avg = statistics.mean(scores.values())
med = statistics.median(scores.values())
min = min(scores.values())
max = max(scores.values())
range = max - min
stddev = statistics.stdev(scores.values())

results.write("\n\n\nStats of accuracies across all features\n")
results.write("------------------------------------------------\n\n")
results.write("Average: "+str(avg)+"\n")
results.write("Median: "+str(med)+"\n")
results.write("Minimum: "+str(min)+"\n")
results.write("Maximum: "+str(max)+"\n")
results.write("Range: "+str(range)+"\n")
results.write("Standard dev: "+str(stddev)+"\n")

