import os

import pandas as pd
import numpy as np

import json

import Screen.Local
from Screen.GlobalLP import LPconstrainedAE
from evaluation.eval_methods import evaluate_parameter_file
from evaluation.file_manipulation import search_json
from evaluation.plotter import Plotter

from statsmodels.tsa.arima.model import ARIMA

folder = "data/big"

files = [folder+"/"+file for file in os.listdir(folder) if file[-4:] != "json" and not os.path.isdir(folder+"/"+file)]
for file in files:
    print(file)
    a = pd.read_csv(file , names = ["index","truth","injected","class"] ,header  = 0)

    with open(search_json(file)) as f:
        data = json.load(f)

    labels = [0, 1, 2,500]
    for anom in data.values():
        labels += anom["index_range"][0:min(3,len(anom["index_range"]))]

    labels = np.concatenate((labels, np.random.randint(0, high=len(a["truth"]), size=int(len(a["truth"])/20))), axis=None)

    #labels = np.array([0, 1, 2, 5, 11])  # in the paper add +1
    # algos = [{ "name" : "imr" , "parameters" :{} } ,{ "name" : "imr" , "parameters" :{"tau" : 0.2 ,"p" : 2} } ,
    #          {"name": "imr", "parameters": {"tau": 0.2, "p": 3}},
    #          {"name": "screen", "parameters": {"T": 2}}
    #          ]
    #evaluate(a["injected"],a["truth"],labels=labels, algos=algos)

    const = Screen.Local.screen(np.array((np.arange(len(a["injected"])),a["injected"])).T,SMIN=-2,SMAX=2)

    x = const["repair"].copy()
    diff =   const["repair"] -a["injected"]
    total = []
    current = []
    in_anomaly = False
    up = True
    down = True
    for i in range(len(diff)):
        if diff[i] == 0:
            if  up and down:
                total += [current]
                current = []
                up = False
                down = False

        else:
            if x[i] > x[i-1]:
                up = True
            if x[i] < x[i-1]:
                down = True
            current.append(i)


    #MA example
    from random import random

    # contrived dataset
    # fit model

    #print(total,"toootal")
    for i in range(0,len(total)):
        if len(total[i]) == 0:
            continue
        if i == 0:
            lower_bound = 0
        else:
            if len(total[i-1]) == 0:
                continue
            lower_bound = total[i-1][-1]+1

        data = x[range(0,total[i][0])]
        if(len(data) > 5):
            model = ARIMA(data,order=(5,1,0))
            model_fit = model.fit()
            # make prediction

            yhat = model_fit.predict(len(data), total[i][-1])

            # print(len(yhat), "yyyaht")
            # print("x",x)
            # print(x[ range(total[i][-1]+1,min(len(x),total[i][-1]+1 + total[i][-1] -len(data) ))  ] )
            r = range(total[i][0],total[i][-1]+1)
            x[ r ] = yhat

    print(total)
    plotter = Plotter(a["injected"].copy(),a["truth"] ,title= "|".join(["" ]+[",".join([str(j) for j in i]) for i in total if len(i)>0]))
    plotter.add(const["repair"],"SCREEN2","SCREEN2")

    plotter.add(x,"SCREEN3","SCREEN3")

    plt = plotter.plotsats()
    plt.show()