#-----------------------------------
#--        Catherine Baugher      --
#--       Coverage Algorithm      --
#-----------------------------------
#!/usr/bin/env python
import csv
import operator
import pprint
import sys
from copy import copy

if(len(sys.argv) > 1):
	datset = sys.argv[1]
else:
	datset = input("What is the name of the dataset (looks at ../featurefilter)?: ")
#path = "/fs/project/PHS0293/cancerproj/cimp-noncimp/featurefilter/" + datset + ".csv"
path = "../../featurefilter/" + datset + ".csv"
with open(path,'r') as f:
	it = csv.reader(f)
	listit = list(it)

posset = [listit[0]]
negset = [listit[0]]
poscounts = {}
negcounts = {}
for x in range(1,len(listit)):
	if(listit[x][len(listit[0])-1] == "-1.0"):
		negset.append(listit[x])
	else:
		posset.append(listit[x])

negset[0].append("totals")
posset[0].append("totals")

for x in range(1,len(posset)):
	counter = 0
	for y in range(1,len(posset[0])-3):
		if(posset[x][y] == "1.0"):
			counter += 1
	poscounts[x] = str(counter)

for x in range(1,len(negset)):
	counter = 0
	for y in range(1,len(negset[0])-3):
		if(negset[x][y] == "1.0"):
			counter += 1
	negcounts[x] = str(counter)

for key in poscounts:
	posset[key].append(poscounts[key])

for key in negcounts:
	negset[key].append(negcounts[key])


with open("./posmatrix.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(posset)

with open("./negmatrix.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(negset)

