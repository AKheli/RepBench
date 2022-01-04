import numpy as np
from matplotlib import pyplot as plt
from skopt import gp_minimize
import pandas as pd

from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from Scenarios.metrics import RMSE
from Scenarios.scenario_types.BaseScenario import BaseScenario
from data_methods.Helper_methods import searchfile, get_df_from_file


def select_data(data, truth, samples, sample_offset=0):
    if samples == -1:
        return data , truth
    np.random.seed(20)
    indexes = np.random.randint(len(data), size=samples, dtype=int)
    return data.iloc[indexes, :], truth.iloc[indexes, :]


def bayesian_opt(data, truth, model, fix_params, params_bounds, samples=-1):
    x = params_bounds.values()

    def f(x):
        params = {k: v for k, v in zip(params_bounds.keys(), x)}
        params.update(fix_params)
        model_i = model(**params)
        selected_data, selected_truth = select_data(data, truth, samples)
        model_i.fit(selected_data)
        predicted = pd.DataFrame(model_i.predict(data))
        result = RMSE(predicted, truth, params["cols"])
        return result

    x = gp_minimize(f, x, n_jobs=-1 , n_initial_points  = 100,n_restarts_optimizer=15).x
    params = {k: v for k, v in zip(params_bounds.keys(), x)}
    params.update(fix_params)
    f(x)
    return Search(params)

class Search():
    def __init__(self,best_params):
        self.best_params_ = best_params


#
# if __name__ == "__main__":
#     file_name = searchfile("temp.csv")
#     print(file_name)
#     df = get_df_from_file(file_name)[0]
#     b = BaseScenario()
#     results = b.transform_df(df)["full_set"]
#     truth = results["original"]
#     injected = results["injected"]
#
#     # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     #     print(injected.corr())
#
#     try:
#         truth.drop("class", axis=1)
#         injected.drop("class", axis=1)
#         df = df.drop("class", axis=1)
#     except:
#         pass
#
#     param_grid = {"threshold": list(np.arange(0.5, 3., 0.2)),
#                   "n_components": [1,2],
#                   "delta": [0.5 ** i for i in range(11)],
#                   "component_method" : [  "TruncatedSVD", "svd"   ],
#                     "interpolate_anomalies": [ False,True]
#
#     }
#
#     default_params = {"cols": [0,1,2,3,4,5,6,7,8,9]}
#
#     bayesian_params = bayesian_opt(injected, truth, Robust_PCA_estimator, default_params, param_grid, samples=-1)
#     model_b = Robust_PCA_estimator(**bayesian_params)
#     d, t = select_data(injected, truth, samples=1000)
#     model_b.fit(d)
#     result_b = pd.DataFrame(model_b.predict(injected))
#     truth.plot()
#     plt.show()
#     result_b.plot()
#     plt.show()
#     injected.plot()
#     plt.show()
#     reduced = pd.DataFrame(model_b.reduce(injected))
#     reduced.plot()
#     plt.show()
#
