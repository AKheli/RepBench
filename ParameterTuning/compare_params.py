import numpy as np
import pandas as pd
from sklearn.experimental import enable_halving_search_cv  # noqa

from Injection.inject import scenario_inject
from ParameterTuning.param_tuner import ParamTuner
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_classification import Robust_PCA_classifier
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.Scenario_Types import *
from data_methods.Helper_methods import get_df_from_file

injection_scenario = BASE_SCENARIO
# parameter_tuning = [bayesian_optimization,halving_grid_search,grid_search]

anomaly_type = AMPLITUDE_SHIFT
data_files = ["test.csv"]




def flatten_dict(dict):
    pd.DataFrame()

param_grid = {
    "threshold": np.arange(0.5, 3., 0.2),
    "n_components": (1,8) , # , 4, 5, 6],
     "delta" : [0.5 ** i for i in range(11)],
    # "component_method": ["TruncatedSVD"]
}

param_grid_s = {
    "T": (0,10000),
    "s": [1,2,3 ] , # , 4, 5, 6],
    # "component_method": ["TruncatedSVD"]
}
param_tuner = ParamTuner() #error=precision , classification=True)
param_tuner.add(Robust_PCA_classifier(cols=[0]), tuners=["ba","bc","ha","gr"], param_grid=param_grid)

for file_name in data_files:
    df, name = get_df_from_file(file_name)
    scenario_data = scenario_inject(df, injection_scenario, anomaly_type)
    param_tuner.optimize_scenario_data(scenario_data)
    for tuner in param_tuner.parameter_tuners:
        print(type(tuner).__name__, tuner.best_estimator_)
    param_tuner.save(file_name)
