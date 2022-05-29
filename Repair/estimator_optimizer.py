import itertools

import numpy as np
from skopt import gp_minimize
from Repair.estimator import Estimator
from multiprocessing.pool import ThreadPool as Pool


class EstimatorOptimizer():

    def __init__(self, estim, type):
        self.type = type
        self.estim: Estimator = estim

    def estim_change_copy(self, param_dict):
        estim_copy = type(self.estim)(columns_to_repair=self.estim.columns_to_repair)
        estim_copy.__dict__.update(self.estim.__dict__)
        estim_copy.__dict__.update(param_dict)
        return estim_copy

    def find_optimal_params(self, injected, truth, labels, param_grid):
        if self.type == "bayesian":
            params = self.bayesian(injected, truth, labels, param_grid)
        if self.type == "grid":
            params = self.grid(injected, truth, labels, param_grid)

        return params

    def bayesian(self, injected, truth, labels, param_grid):
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
        param_keys, param_values = param_ranges.keys(), param_ranges.values()

        def f(x):
            estim = self.estim_change_copy(dict(zip(param_keys, x)))
            return -estim.score(injected, truth, labels)

        x = gp_minimize(f, param_values, n_jobs=-1,
                        n_calls=30,
                        n_initial_points=20,
                        n_restarts_optimizer=2,
                        ).x

        return dict(zip(param_keys, x))

    def halvingsearch(self, injected, truth, labels, param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))

        anomaly_array = np.invert(np.isclose(injected, truth)).sum()
        indices = np.arange(len(anomaly_array))[anomaly_array]

        n, m = injected.shape()
        mid = indices[int(len(indices) / 2)]  # make sure we have some anomaly

        start_res_half = 20
        comb_nbr = len(param_combinations)
        n_iterations = int(np.log(comb_nbr))

        def f(params, indices=None):
            estim = self.estim_change_copy(params)
            if indices is None:
                estim.score(injected, truth, labels)
            else:
                score_ = estim.score(injected[indices, :], truth[indices, :], labels[indices, :])
            return score_

        with Pool(10) as p:
            for i in range(n_iterations):
                if len(param_combinations) <= 10:
                    scores = np.array(p.map(f, param_combinations))
                    index = np.argmax(scores)
                    optimal_params = param_combinations[index]

                indices = range(max(0, mid - 2 ** i * start_res_half), min(n, mid + 2 ** i * start_res_half))
                scores = np.array(p.map(lambda params: f(params, indices), param_combinations))
                param_combinations = [x for i, (_, x) in
                                      enumerate(sorted(zip(scores, param_combinations), reverse=True)) if
                                      i < len(param_combinations + 1) / 2]

        return optimal_params

    def grid(self, injected, truth, labels, param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        print("params:", param_combinations)

        # for score in ["full_rmse","mae","partial_rmse"]:
        #    self.estim.set_score_f(score)
        def f(params):
            estim = self.estim_change_copy(params)
            score_ = estim.score(truth, injected, labels)
            return score_

        with Pool(8) as p:
            scores = np.array(p.map(f, param_combinations))
            index = np.argmax(np.array(scores))

            optimal_params = param_combinations[index]
        # print(list(zip(param_combinations,scores)))
        # print(optimal_params, self.estim_change_copy(optimal_params).score(injected,truth,labels))
        # print(optimal_params)
        return optimal_params
