import argparse
import sys
import pandas as pd
import numpy as no

from Injector import *

parser = argparse.ArgumentParser()
parser.add_argument("-data","-d" ,nargs=1, type=str ,  required=True)
parser.add_argument('-sep',nargs=1, default=[','])
parser.add_argument('-datacol',"-col" , nargs=1, default=[0] ,type=int )

parser.add_argument('-save',  nargs=1, type=str , default=False )
parser.add_argument('-plot', action='store_true')
parser.add_argument('-whitoutlegend', action='store_false')

#anomalies
parser.add_argument("-type" ,nargs=1, type=str , action="extend")
parser.add_argument("-length" ,nargs=1, type=int , action="extend")
parser.add_argument("-factor", nargs=1, type=int,  action="extend")
parser.add_argument("-number_of_iterations" ,nargs=1, type=int,  action="extend")
parser.add_argument("-direction", nargs=1, type=str,  action="extend",required=False)

args = parser.parse_args()
print("seeeeeeeeeeeep" ,args.sep)

data = pd.read_csv(args.data[0], sep=args.sep[0] , header = None)
header = None
#check if first data col has string
for i in data.iloc[0]:
    if isinstance(i, str):
        header = 0

data = pd.read_csv(args.data[0], sep=args.sep[0] , names=list(range(data.shape[1])) , header = header)
print(data)

injector = Anomalygenerator(np.array(data[int(args.datacol[0])]))


anomalies = []
current_dict = {}
lastkey = None

for x in sys.argv[1:]:
    if x[0] == "-":
        if x[1] == "t":
            anomalies.append(current_dict)
            current_dict = dict()
        try:
            lastkey = [s for s in vars(args).keys() if  s.startswith(x[1:])][0]
        except:
            pass
    else:
        current_dict[lastkey] = x

anomalies.append(current_dict)
anomalies = anomalies[1:]

for anom in anomalies:
    type = anom["type"]
    print(anom.get("-number_of_iterations",1))
    if type[0] == "a":
        #length=10, factor=8, starting_index=None,  number_of_ranges=1 , std_range=(-10, 10),directions=[1, -1]
        injector.add_amplitude_shift(length=int(anom.get("length",10)),factor=int(anom.get("factor",8)),number_of_ranges =int(anom.get("number_of_iterations",1)))
    elif type[0] == "d":
        injector.add_distortion(length=int(anom.get("length",10)),factor=int(anom.get("factor",8)),number_of_ranges =int(anom.get("number_of_iterations",1)))
    elif type[0] == "g":
        injector.add_growth(length=int(anom.get("length",10)),factor=int(anom.get("factor",8)),number_of_ranges =int(anom.get("number_of_iterations",1)))
    elif type[0] == "e":
        injector.add_distortion(length=1,factor=int(anom.get("factor",8)),number_of_ranges =int(anom.get("number_of_iterations",1)))
    else:
        print(f"anomaly type {type[0]} not recognized")

if(args.plot):
    injector.plot(legend=args.whitoutlegend)

if(args.save):
    injector.save(args.save[0])

