import sys

import numpy as np
import pandas as pd
#exec(open('__main__.py').read())
from Injector import *

outputfile = None


print("Enter data file path")
print("example Data/SAG.csv")

while(True):
    try:
        path = input()
        if path[-4:] == "json":
            data = pd.read_json(path)
            print(data)
        else:
            data = pd.read_csv(path,header=0, sep=';')
            print(data)
            print("pick delimiter and header (infer or index)")
            sep = input()
            header = input()
            if(header.isnumeric()):
                header = int(header)
            data = pd.read_csv(path, sep=sep)
            data = pd.read_csv(path,names=list(range(data.shape[1])), sep=sep, header = header)
            print(data)


        outputfile = data.copy
        break
    except FileNotFoundError:
        print("no such file found , try agian")

while(True):
    try:
        if("ts_name" in data):
            print("select ts_name")
            path = input()
            data = data[data["ts_name"] == path]
        print("select column")
        col = input()
        data = data[int(col)]

        injector = Anomalygenerator(np.array(data))
        break
    except KeyError as e :
        print(e)
        print("no such name found, try agian")
print("injector initialized")



print("select datarow and initialize the injector , inector(datarow)",
"\inject the anomalies and save :", '\n outputfile["injected"] = injector.get_injected_series()'
,'\noutputfile.to_csv("injected")')



