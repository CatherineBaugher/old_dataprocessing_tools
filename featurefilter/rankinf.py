import os
import csv
import math
import statistics

#open original
inpdat = "../../coadreadDAT.csv"
with open(inpdat,'r') as f:
	it = csv.reader(f)
	orig = list(it)

#open filtered file
with open("./filtered_infogain005.csv","r") as f:
	it = csv.reader(f)
	listit = list(it)



ranks = open("./rankedinf.txt","w")

#first find entropy of S
fore = back = 0
tot = len(orig) - 1
endcol = len(orig[0]) - 1
for x in range(1,len(orig)): #take a look at each row
	if float(orig[x][endcol]) == -1.0: #found background
		back += 1
	elif float(orig[x][endcol]) == 1.0: #found foreground
		fore += 1
entS = -fore/tot * math.log((fore/tot),2) - back/tot * math.log((back/tot),2)


#rank each column for info gain
scores = {}
endcol = len(listit[0]) - 1
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
	scores[listit[0][y]] = entS - (Rtot/tot)*entR - (Ltot/tot)*entL

for key,value in sorted(scores.items(), key=lambda v:(-v[1],v[0])):
	ranks.write(key + " : " + str(value) + "\n")


