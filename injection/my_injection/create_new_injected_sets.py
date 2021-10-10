import pandas as pd
import numpy as np

from  Injector import *

datafile = None
dataoutput = None
data = None
injector = None
outputfile = None

print("select and store data file into variable datafile and run loadfromfile")

def loadfromfile():
    global data
    global injector
    global outputfile

    if datafile is None:
        print("variable datafile is None")
        return
    if datafile[-4:] == "json":
        data = pd.read_json(datafile)

    else:
        data = pd.read_json(datafile)

    print("select data as a single data row and run generate_injector")
    print(data)
    outputfile = data.copy

def generate_injector():
    global data
    global injector
    data = np.array(data)
    injector = Anomalygenerator(data)
    print("start injecting with the injector , use injector.plot() to vizalize data")


def save():
    outputfile["injected"] = injector.get_injected_series()
    outputfile.to_csv("injected")








