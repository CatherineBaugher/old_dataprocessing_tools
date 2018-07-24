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

inpdat = "../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)


percent = float(input("What percent would you like to filter by?")) * .01



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


#.25% of size, how many?
limit = percent * len(listit[0])
x = 0
accs = []
keep = [0] #gotta keep the sample lables...

print(str(min(scores.values())))

for key,value in sorted(scores.items(), key=lambda v:(-v[1],v[0])):
	if x <= limit:
		keep.append(key)
		accs.append(value)
		x += 1
	else:
		break;

keep.append(len(listit[0])-1) #need to also keep the classifications
newdatset = [[row[c] for c in keep] for row in listit]

print("col # of new:",len(newdatset[0]))

with open("filtered_infogain" + str(percent)[3:] + ".csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newdatset)

