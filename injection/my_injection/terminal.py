import argparse
import sys
import pandas as pd
import numpy as no

from Injector import *

parser = argparse.ArgumentParser()
parser.add_argument("-data", nargs=1, type=str ,  required=True)
parser.add_argument('-sep',nargs=1, default=',')
parser.add_argument('-datacol',nargs=1, default=0 ,type=int )

parser.add_argument('-save',  nargs=1, type=str )
parser.add_argument('-plot', action='store_true')
parser.add_argument('-legendoff', action='store_false')



#anomalies
parser.add_argument("-type" ,nargs=1, type=str , action="extend")
parser.add_argument("-length" ,nargs=1, type=int , action="extend")
parser.add_argument("-factor", nargs=1, type=int,  action="extend")
parser.add_argument("-times", nargs=1, type=int,  action="extend")
parser.add_argument("-direction", nargs=1, type=str,  action="extend",required=False)





args = parser.parse_args()
print(args.data)
data = pd.read_csv(args.data[0], sep=args.sep)
data = pd.read_csv(args.data[0], sep=args.sep , names=list(range(data.shape[1])))


injector = Anomalygenerator(np.array(data[int(args.datacol[0])]))



anomalies = []
current_dict = {}
lastkey = None
for x in sys.argv[1:]:
    if x == "-type":
        anomalies.append(current_dict)
        current_dict = dict()

    if x[0] == "-":
        lastkey = x
    else:
        current_dict[lastkey] = x

anomalies.append(current_dict)
anomalies = anomalies[1:]

for anom in anomalies:
    type = anom["-type"]

    if type[0] == "a":
        #length=10, factor=8, starting_index=None,  number_of_ranges=1 , std_range=(-10, 10),directions=[1, -1]
        injector.add_amplitude_shift(length=int(anom.get("-length",10)),factor=int(anom.get("-factor",8)),number_of_ranges =int(anom.get("-times",1)))
    if type[0] == "d":
        injector.add_distortion(length=int(anom.get("-length",10)),factor=int(anom.get("-factor",8)),number_of_ranges =int(anom.get("-times",1)))
    if type[0] == "g":
        injector.add_growth(length=int(anom.get("-length",10)),factor=int(anom.get("-factor",8)),number_of_ranges =int(anom.get("-times",1)))

if(parser.parse_args().plot):
    injector.plot(legend=parser.parse_args().legendoff)