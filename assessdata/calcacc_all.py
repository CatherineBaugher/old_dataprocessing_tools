# CALCACC_ALL.PY
# Reports statistics of accuracies across
# across all features
#!/usr/bin/env python

import statistics
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
	falseneg = falsepos = trueneg = truepos = 0
	left = []
	right = []
	for x in range(1,endrow): #look at each sample
		if(float(listit[x][y]) == 1.0):
			right.append((listit[x][0],float(listit[x][endcol])))
		elif(float(listit[x][y]) == 0.0):
			left.append((listit[x][0],float(listit[x][endcol])))

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
		if(float(listit[x][endcol]) == 1.0):
			if(classif[listit[x][0]] == 1.0):
				truepos += 1
			elif(classif[listit[x][0]] == -1.0):
				falsepos += 1
			else:
				print("ERROR1")
		elif(float(listit[x][endcol]) == -1.0):
			if(classif[listit[x][0]] == 1.0):
				falseneg += 1
			elif(classif[listit[x][0]] == -1.0):
				trueneg += 1
			else:
				print("ERROR2")
		else:
			print(listit[x][endcol])
	#print(str(falseneg),str(falsepos),str(truepos),str(trueneg),"\n")
	accuracy = (falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos)
	scores[y] = accuracy

#now come up with stats
avg = statistics.mean(scores.values())
med = statistics.median(scores.values())
min = min(scores.values())
max = max(scores.values())
range = max - min
stddev = statistics.stdev(scores.values())

results = open("./accstats_all.txt","w")
results.write("Stats of accuracies across all features\n")
results.write("------------------------------------------------\n\n")
results.write("Average: "+str(avg)+"\n")
results.write("Median: "+str(med)+"\n")
results.write("Minimum: "+str(min)+"\n")
results.write("Maximum: "+str(max)+"\n")
results.write("Range: "+str(range)+"\n")
results.write("Standard dev: "+str(stddev)+"\n")

