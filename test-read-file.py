import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import collections

headers=['date', 'api', 'info', 'modelType', 'action', 'docType', 'userID', 'other']

data=pd.read_csv('info.log', parse_dates={"Datetime": [0]}, names=headers)

#print(data['Datetime'])
#print(data['action'])

nModelType=collections.Counter(data['modelType'])
print(nModelType)
naction=collections.Counter(data['action'])
print(naction)
ndocType=collections.Counter(data['docType'])
print(ndocType)
nuserID=collections.Counter(data['userID'])
print(nuserID)

print('\n\n')

print(data['action'].value_counts()[:])



#f = open("info.log","r") #opens file
#print(f.read())
#myList = []
#for line in f:
#    myList.append(line)
#    print(line)
#print(myList)