import csv
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split
from graphviz import Source # for drawing decision tree
#from IPython.display import SVG # for drawing decision tree
import numpy as np
import pandas
import random
import math

rawData = pandas.read_csv("../../PANCANcoadread_control.csv", delimiter=',', skipinitialspace=True, warn_bad_lines=True, index_col=0) 
# change lows and neg to false, high to true
rawData.loc[rawData['class'] == 2.0, 'class'] = 0.0
rawData.loc[rawData['class'] == -1.0, 'class'] = 0.0
rawData = rawData.astype('bool') # convert to bools
foreground = rawData.loc[rawData['class'] == True].drop('class', axis = 1) # split into forground and backgorund
background = rawData.loc[rawData['class'] == False].drop('class', axis = 1)

posCounts = foreground.sum(axis=0) #produces list of sum of occurances in foregorund for each column
negCounts = background.sum(axis=0)

plt.scatter(list(map(lambda x: x + random.random() -.5, posCounts)), list(map(lambda x: x + random.random() -.5, negCounts)))
#plt.scatter(posCounts, negCounts, alpha=0.3)
plt.title("CIMP-High vs. non-CIMP-High Occurrences")
# plt.scatter(list(map(lambda x: x + random.random() -.5, posCounts)), list(map(lambda x: x + random.random() -.5, negCounts)), alpha=0.3)
plt.xlabel("Number of positive occurrences")
plt.ylabel("Number of negative occurrences")
plt.ylim(-1,30)
plt.xlim(-0.5,20)
plt.savefig('figure1.png')
