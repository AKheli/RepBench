import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.experimental import enable_halving_search_cv  # noqa

from Injection.inject import scenario_inject
from ParameterTuning.param_tuner import ParamTuner
from Repair.Robust_PCA.robust_PCA_estimator import Robust_PCA_estimator
from Scenarios.Anomaly_Types import *
from Scenarios.scenario_types.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.scenario_types.Scenario_Types import *
from data_methods.Helper_methods import get_df_from_file

injection_scenario = SCENARIO_CONSTRUCTORS[BASE_SCENARIO]
# parameter_tuning = [bayesian_optimization,halving_grid_search,grid_search]

anomaly_type = DISTORTION
data_files = ["YAHOO.csv","batch10.txt" , "TemperatureTS8.csv" , "BAFU20K.txt" ]  # , , "motion_normal.txt", "TemperatureTS8.csv", "BAFU.txt","batch10.txt"]

param_grid_1 = {
    "n_components": [1, 2, 3, 4,5,6,7],  # , 4, 5, 6],
    "delta":  np.linspace(0.001,1,num=20),
    #"interpolate_anomalies": [True],
    # "component_method": ["TruncatedSVD"]
}

param_grid_2 = {
    "threshold":  np.arange(0.1, 3.8 , 0.2),
    "n_components": [1, 2, 3, 4,5],  # , 4, 5, 6],
    "delta":  [0.5 ** i for i in range(8)],
    "interpolate_anomalies": [False,True],
    # "component_method": ["TruncatedSVD"]
}

# param_grid_try = {
#     "delta":  [0.5 ** i for i in range(8)],
#     #"fit_on_truth": [False,True],
#     "interpolate_anomalies": [False,True],
#     # "component_method": ["TruncatedSVD"]
# }


# param_grid_s = {
#     "T": (0, 10000),
#     "s": [1, 2, 3],  # , 4, 5, 6],
#     # "component_method": ["TruncatedSVD"]
# }

#check file names
for file_name in data_files:
    df, name = get_df_from_file(file_name)
    del df

tuners = []
for i, file_name in enumerate(data_files):
    param_tuner = ParamTuner(n_jobs=1)  # error=precision , classification=True)
    param_tuner.add(Robust_PCA_estimator(cols=[0]), tuner="ba" , name  = "ba_no_t"
                    , param_grid=param_grid_1)
    # param_tuner.add(Robust_PCA_estimator(cols=[0]), tuner="gr", name="gr_no_t"
    #                  , param_grid=param_grid_1)
    # param_tuner.add(Robust_PCA_estimator(cols=[0]), tuner="du"
    #                 , param_grid=param_grid_1)
    # param_tuner.add(Robust_PCA_estimator(cols=[0]), tuner="gn"
    #                 , param_grid=param_grid_1)
    

    # param_tuner.add(Robust_PCA_estimator(cols=[0]), tuners=["bc", "gr", "ha"]  # "ba",
    #                 , param_grid=param_grid , cv = CV_splitter())
    df, name = get_df_from_file(file_name)
    scenario_data = injection_scenario(file_name, {"anomaly_type" : anomaly_type}, train_test_split=0.5)
    param_tuner.optimize_scenario(scenario_data)
    tuners.append(param_tuner)

values , ticks ,labels =[] , [] , []
for i , tuner in enumerate(tuners):
    l = ["dotted", "dashdot", "dashed", "solid"] * 10
    range_ = [i * 2, i * 2 + 1]
    plt.gca().set_prop_cycle(None)
    for t_m in tuner.parameter_tuners:
        fit_time = t_m["fit_time"]
        name = t_m["name"]
        r = t_m["scores"]

        plt.plot(range_, r.values(), ls=l.pop(), marker='x', label=f"{name}({round(fit_time)}s)")

        values +=  r.values()
        ticks+= range_
        labels += [f'{key}_{data_files[i]}' for key in  r.keys()]
    if i == 0:
        plt.legend()

plt.ylim((0, 1))
plt.xticks(ticks, labels, rotation=45)
plt.ylabel("error ratio")
plt.show()


ticks ,labels =[] , []
for i , tuner in enumerate(tuners):
    l = ["dotted", "dashdot", "dashed", "solid"] * 10
    range_ = [i]
    plt.gca().set_prop_cycle(None)
    for t_m in tuner.parameter_tuners:
        name = t_m["name"]
        r = t_m["fit_time"]
        plt.plot(range_, r, ls=l.pop(), marker='x', label=f"{name}")

        ticks+= range_
        labels += [f'{data_files[i]}']
    if i == 0 :
        plt.legend()

plt.xticks(ticks, labels, rotation=45)
plt.ylabel("fit time")
plt.show()


    # for tuner in param_tuner.parameter_tuners:
    #     print(type(tuner).__name__, tuner.best_estimator_)
    # param_tuner.save(file_name)
# except:
#     try:
#         param_tuner.save(f'error_{file_name}')
#     except:
#         pass
