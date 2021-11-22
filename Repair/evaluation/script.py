import os

import pandas as pd
import numpy as np

import json

from Repair.repair_algos.IMR import imr2
from Repair.repair_algos.Screen.Labelinterpolation import interpolate
from Repair.res import search_json
from Repair.res import Plotter

folder = "../Data/big"
print(os.listdir())
files = [folder+"/"+file for file in os.listdir(folder) if file[-4:] != "json" and not os.path.isdir(folder+"/"+file)]
print(files)
for file in files:
    print(file)
    a = pd.read_csv(file , names = ["index","truth","injected","class"] ,header  = 0)

    with open(search_json(file)) as f:
        data = json.load(f)

    labels = [0, 1, 2]
    for anom in data.values():
        labels += anom["index_range"][0:min(3,len(anom["index_range"]))]

    labels = np.concatenate((labels, np.random.randint(0, high=len(a["truth"]), size=int(len(a["truth"])/20))), axis=None)

    #labels = np.array([0, 1, 2, 5, 11])  # in the paper add +1
    # algos = [{ "name" : "imr" , "multiple_algos" :{} } ,{ "name" : "imr" , "multiple_algos" :{"tau" : 0.2 ,"p" : 2} } ,
    #          {"name": "imr", "multiple_algos": {"tau": 0.2, "p": 3}},
    #          {"name": "screen", "multiple_algos": {"T": 2}}
    #          ]
    #evaluate(a["injected"],a["truth"],labels=labels, algos=algos)

    const = Repairalgos.Screen.Local.screen(np.array((np.arange(len(a["injected"])), a["injected"])).T, SMIN=-2, SMAX=2)

    inter = interpolate(a["injected"],a["truth"],labels)

    imr_repair = imr2(a["injected"],a["truth"],labels)

    plotter = Plotter(a["injected"].copy(),a["truth"] ,title= "test",labels=labels)
    #plotter.add(const["repair"],"SCREEN2","SCREEN2")
    plotter.add(imr_repair["repair"],"imr","imr")
    plotter.add(inter["repair"],"inter","intre")
    plotter.add(inter["interline"],"line","line")
    plotter.add(inter["above"],"line2","line2")
    plotter.add(inter["below"],"line3","line3")

    plt = plotter.plotsats()
    plt.show()