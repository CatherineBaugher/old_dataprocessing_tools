# CALCSAMPINFO.PY
# determines number of CIMP+ and CIMP-
# determines number of features occur in it
#!/usr/bin/env python

import statistics
import csv
from operator import itemgetter

inpdat = "../../coadreadDAT.csv"

with open(inpdat,'r') as f:
	it = csv.reader(f)
	listit = list(it)

endcol = len(listit[0])-1
endrow = len(listit)
neg = pos = tot = 0
for x in range(1,endrow):
	if(float(listit[x][endcol]) == 1.0):
		pos += 1
	elif(float(listit[x][endcol]) == -1.0):
		neg += 1
	tot += 1

print("Total: " + str(tot))
print("CIMP: " + str(pos))
print("non-CIMP: " + str(neg))
