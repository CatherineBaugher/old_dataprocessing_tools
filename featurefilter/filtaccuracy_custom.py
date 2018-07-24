# -----------------------------------------------------------------------------$
# filtaccuracy1.py
# result is new dataset with only features in top 1% accuracy
# if it marks 0, this is interpretted -1, if 1, it is interpretted 1.
# then based on the actual foreground/background, accuracy is computed
# -----------------------------------------------------------------------------$
import os
import csv
import statistics

inpdat = "../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)

percent = float(input("What percent would you like to filter by?")) * .01

print("col # of old:",len(listit[0]))
ranks = open("./rankedacc.txt","w")
scores = {}
ability = {} #use to store FN, FP, TN, TP
endcol = len(listit[0])-1
endrow = len(listit)
for y in range(1,endcol): #for each mut, minus class
	falseneg = 0
	falsepos = 0
	trueneg = 0
	truepos = 0
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
		majl = 1.0
	try:
		majr = statistics.mode(x[1] for x in right)
	except:
		majr = 1.0

	#now classify all samples under the majority...
	classif = {}
	for x in left:
		classif[x[0]] = majl
	for x in right:
		classif[x[0]] = majr
	#	if(majr != -1.0):
	#		print("hurrah", str(majr))
	#print(classif)
	#now score the results...
	fpsamps = []
	tpsamps = []
	for x in range(1,endrow):
		if(classif[listit[x][0]] == 1.0):
			if(float(listit[x][endcol]) == 1.0):
				truepos += 1
				tpsamps.append(listit[x][0])
			elif(float(listit[x][endcol]) == -1.0):
				falsepos += 1
				tpsamps.append(listit[x][0])
			else:
				print("ERROR1")
		elif(classif[listit[x][0]] == -1.0):
			if(float(listit[x][endcol]) == 1.0):
				falseneg += 1
			elif(float(listit[x][endcol]) == -1.0):
				trueneg += 1
			else:
				print("ERROR2")
		else:
			print("ERROR3")
			print(listit[x][endcol])
	#print(str(falseneg),str(falsepos),str(truepos),str(trueneg),"\n")
	accuracy = 1-((falseneg+falsepos)/(trueneg+falseneg+falsepos+truepos))
	scores[y] = accuracy
	tmpTup1 = (falsepos,fpsamps)
	tmpTup2 = (truepos,tpsamps)
	myTup = (falseneg,falsepos,trueneg,truepos)
	ability[y] = myTup

limit = percent * len(listit[0])
x = 0
accs = []
keep = [0] #gotta keep the sample lables...
newcsv = [["","false_negative","false_positive","true_negative","true_positive"]]
print(str(max(scores.values())))
for key,value in sorted(scores.items(), key=lambda v:(-v[1],v[0])):
	if x <= limit:
		keep.append(key)
		accs.append(value)
		ranks.write(listit[0][key] + " : " + str(value) + "\n")
		newcsv.append([listit[0][key],ability[key][0],ability[key][1][0],ability[key][2],ability[key][3][0]])
		x += 1
	else:
		break;
keep.append(len(listit[0])-1) #need to also keep the classifications

newdatset = [[row[c] for c in keep] for row in listit]

print("col # of new:",len(newdatset[0]))
with open("filtered_accuracy" + str(percent)[3:] + ".csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newdatset)

#output stats of accuracy filter
with open("./statsofaccfilt.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newcsv)
