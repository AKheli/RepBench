import itertools

import numpy as np
from skopt import gp_minimize
from Repair.estimator import Estimator
from multiprocessing.pool import ThreadPool as Pool

class EstimatorOptimizer():

    def __init__(self, estim ,type):

        self.type = type
        self.estim : Estimator = estim

    def estim_change_copy(self,param_dict):
        estim_copy = type(self.estim)(columns_to_repair =self.estim.columns_to_repair)
        estim_copy.__dict__.update(self.estim.__dict__)
        estim_copy.__dict__.update(param_dict)
        return estim_copy

    def find_optimal_params(self, injected,truth,labels,param_grid):
        if self.type == "bayesian":
            params =  self.bayesian(injected,truth,labels,param_grid)
        if self.type == "grid":
            params =  self.grid(injected,truth,labels,param_grid)

        print("PARAAARMS" ,params)
        return params

    def bayesian(self,injected,truth,labels,param_grid):
        param_ranges = {}

        # convert list to ranges
        for k, params_list in param_grid.items():
            if len(set(params_list)) == 1:
                param_ranges[k] = [params_list[0]]

            else:
                try:
                    [float(i) for i in params_list]  # check if all items are numerical arguments
                    param_ranges[k] = (min(params_list), max(params_list))
                except:
                    param_ranges[k] = params_list
        print(param_ranges)
        param_keys, param_values = param_ranges.keys(), param_ranges.values()

        def f(x):
            estim = self.estim_change_copy(dict(zip(param_keys, x)))
            return  -estim.score(injected, truth , labels)

        x = gp_minimize(f, param_values, n_jobs=-1
                        , n_calls=30,
                        n_initial_points=20,
                        n_restarts_optimizer=2,
                        ).x

        return dict(zip(param_keys, x))


    def grid(self, injected, truth,labels, param_grid):

        def f(params):
            estim = self.estim_change_copy(params)
            score_ = estim.score(truth, injected, labels)
            return score_

        with Pool(8) as p:
            param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
            scores = np.array(p.map(f,param_combinations))
            index = np.argmax(np.array(p.map(f,param_combinations)))

            optimal_params = param_combinations[index]

        return optimal_params