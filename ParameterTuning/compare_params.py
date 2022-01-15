import numpy as np
import pandas as pd
from sklearn.experimental import enable_halving_search_cv  # noqa

from Injection.inject import scenario_inject
from ParameterTuning.cv_split_generation import  CV_splitter
from ParameterTuning.param_tuner import ParamTuner
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_classification import Robust_PCA_classifier
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.Scenario_Types import *
from data_methods.Helper_methods import get_df_from_file

injection_scenario = VARY_TS_LENGTH
# parameter_tuning = [bayesian_optimization,halving_grid_search,grid_search]

anomaly_type = AMPLITUDE_SHIFT
data_files = ["TemperatureTS8.csv"]  # , , "motion_normal.txt", "TemperatureTS8.csv", "BAFU.txt","batch10.txt"]


def flatten_dict(dict):
    pd.DataFrame()


param_grid = {
    "threshold":(0.1,3.0) ,# np.arange(0.5, 3., 0.2),
    "n_components": [1, 2, 3, 4, 5, 6, 7],  # , 4, 5, 6],
    "delta": [0.5 ** i for i in range(11)],
    "fit_on_truth": [True,False],
    # "component_method": ["TruncatedSVD"]
}

param_grid_s = {
    "T": (0, 10000),
    "s": [1, 2, 3],  # , 4, 5, 6],
    # "component_method": ["TruncatedSVD"]
}

for file_name in data_files:
    param_tuner = ParamTuner()  # error=precision , classification=True)
    param_tuner.add(Robust_PCA_estimator(cols=[0]), tuners=[ "bc" , "ba", "gr" , "ha"]  # "ba",
                    , param_grid=param_grid)
    # param_tuner.add(Robust_PCA_estimator(cols=[0]), tuners=["bc", "gr", "ha"]  # "ba",
    #                 , param_grid=param_grid , cv = CV_splitter())
    df, name = get_df_from_file(file_name)
    scenario_data = scenario_inject(df, injection_scenario, anomaly_type, train_split=0.5)
    param_tuner.optimize_scenario(scenario_data)
    # for tuner in param_tuner.parameter_tuners:
    #     print(type(tuner).__name__, tuner.best_estimator_)
    # param_tuner.save(file_name)
# except:
#     try:
#         param_tuner.save(f'error_{file_name}')
#     except:
#         pass
