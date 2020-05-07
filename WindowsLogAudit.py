import csv
import os
import sys
import math
import time
import pandas
from os.path import isfile, join
from sqlalchemy import create_engine

def printDic(dictionary):
    for item in dictionary:
        print("%s : "% item, dictionary[item])


typeCount = {
    "Warning":0,
    "Error":0,
    "Information":0,
    "Critical":0,
    "Audit Success":0,
    "Audit Failure":0
}

eventIdCount = {}



data = pandas.DataFrame()

script_dir = os.path.dirname(__file__)
files = os.listdir('CSVs/')
for log in files:
    rel_path = "CSVs/" + log
    abs_file_path = os.path.join(script_dir, rel_path)
    data = data.append(pandas.read_csv(abs_file_path, skiprows=1, skipfooter=1, engine='python', names=["Type","Date_and_Time","Source","Event_ID","Task_Category","Description"]))
    

#print(data.head())

logType = data.Type.tolist()
typeList = ("Warning", "Error", "Information", "Critical","Audit Success","Audit Failure")
eventIds = data.Event_ID.tolist()

for event in eventIds:
    if (math.isnan(event)):
        continue
    elif event in eventIdCount:
        eventIdCount[event] = eventIdCount[event]+1
    else:
        eventIdCount[event] = 1
    
for type in logType:
    if any(s in type for s in typeList):
        typeCount[type] = typeCount[type] + 1

print("\nLog Types")
printDic(typeCount)
print("\nEventIDs")
printDic(eventIdCount)
#print(data)


engine = create_engine('sqlite://', echo=False)
print("Creating Database")
#time.sleep(1)
data.to_sql('entries', con=engine)
#print("Done")
#time.sleep(1)

results = engine.execute("SELECT * FROM entries WHERE Type='Audit Success' AND Description LIKE '%log on%' ORDER BY Date_and_Time ASC").fetchall()
#results = engine.execute("SELECT Description FROM entries WHERE Description LIKE '%fail%'  ORDER BY Date_and_Time ASC").fetchall()

for e in results:
    print(str(e).strip("(),'").replace('\\n','').replace('\\r',' ').replace('\\t',' ')+'\n')

print("Number of matching queries: "+str(len(results)))




