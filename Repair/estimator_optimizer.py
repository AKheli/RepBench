import itertools

import numpy as np
from skopt import gp_minimize
from Repair.estimator import Estimator
from multiprocessing.pool import ThreadPool as Pool


class EstimatorOptimizer():
    def __init__(self, estim, opt_method , error_score):
        self.error_score = error_score
        self.opt_method = opt_method
        self.estim: Estimator = estim

    def estim_change_copy(self, param_dict):
        estim_copy = type(self.estim)()
        estim_copy.__dict__.update(self.estim.__dict__)
        estim_copy.__dict__.update(param_dict)
        return estim_copy

    def find_optimal_params(self,repair_inputs, param_grid):
        columns_to_repair = repair_inputs["columns_to_repair"]
        assert not np.allclose(repair_inputs["injected"].values[:, columns_to_repair], repair_inputs["truth"].values[:,columns_to_repair])

        """ minimized the estimators repair score over the fiven parameter range"""

        if self.opt_method == "bayesian":
            params = self.bayesian(repair_inputs, param_grid)
        if self.opt_method == "grid":
            params = self.grid(repair_inputs, param_grid)

        return params

    def bayesian(self, repair_inputs,  param_grid):

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

        self.counter = 0
        import sys
        def f(x):
            self.counter += 1
            sys.stdout.write(f"\rbayesian opt search {self.counter / 30 * 100:.1f} %", )
            estim = self.estim_change_copy(dict(zip(param_keys, x)))
            score= estim.scores(**repair_inputs)[self.error_score]
            return score

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

    def grid(self, repair_inputs, param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        print("params:", param_combinations)
        self.counter = 0
        import sys
        def f(params):
            self.counter+=1
            sys.stdout.write(f"\rgrid search {self.counter/ len(param_combinations) * 100:.1f} %",)
            estim = self.estim_change_copy(params)
            score_ = estim.scores(**repair_inputs)[self.error_score]
            return score_

        with Pool(8) as p:
            scores = np.array(p.map(f, param_combinations))
            index = np.argmin(np.array(scores))
            optimal_params = param_combinations[index]

        return optimal_params
