import os
import csv

inpdat = "../../../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)


selections = open("./selected.txt","r")
keep = [0] #gotta keep the sample lables...
for line in selections:
	word = line.split()[0]
	keep.append(listit[0].index(word))

keep.append(len(listit[0])-1)

newdatset = [[row[c] for c in keep] for row in listit]

print("col # of new:",len(newdatset[0]))
with open("../../filtered_sklearn20.csv","w") as fun:
	writer = csv.writer(fun)
	writer.writerows(newdatset)
