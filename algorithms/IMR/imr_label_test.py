import math

import matplotlib
from matplotlib import pyplot as plt

import Scenarios.ScenarioConfig as sc

#vary
# sc.label_seed
# sc.label_rate
# sc.anomstartlabelrate
from Scenarios.data_generation import full_train_test
from algorithms import IMR_estimator, Robust_PCA_estimator

scen = "base"
data_names = ["bafu","elec","msd"]
a_type = "shift"

seed_counter = 0



out_put = {}
for data_name in data_names:
    out_put[data_name] = {}
    pca_estimator: Robust_PCA_estimator = Robust_PCA_estimator()
    for label_rate in [0.01,0.02,0.05,0.1,0.2,0.3]:
        out_put[data_name][label_rate] = []
        sc.label_rate = label_rate
        for i in range(100):
            seed_counter += 1
            sc.label_seed = seed_counter
            sc.anomstartlabelrate = 0
            train , test = full_train_test(data_name,a_type, max_n_rows = 50000)
            if i == 0:
                rpca_scores = pca_estimator.scores(**train.repair_inputs)
                rpca_rmse = rpca_scores["full_rmse"]

            imr_estim : IMR_estimator = IMR_estimator()
            errors = imr_estim.scores(**train.repair_inputs)
            rmse = errors["full_rmse"]
            out_put[data_name][label_rate].append(rmse)

    labels , data = [*zip(*out_put[data_name].items())]
    d_ = out_put[data_name]
    print(data_name)
    print("{"+ f"{[f'({key} u {x})' for key,l_ in d_.items() for x in l_ ]}"[1:-1].replace("'","").replace(",","").replace("u",",")+"}")
    print( ((k ,sum(x)/len(x)) for k,x in d_.items()))
    plt.plot(data, lw = 0 , marker = "x" , color = "black")
    #plt.hlines(rpca_rmse,xmin=0,xmax=len(data))
    plt.xticks(range(0, len(labels) ), labels)
    fig = plt.gcf()
    #matplotlib.use('pgf')
    #fig.savefig('norm.pgf', format='pgf')
    plt.show()