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

        if self.opt_method == "halving":
            params = self.halvingsearch(repair_inputs, param_grid)

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

    def halvingsearch(self, repair_inputs, param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        columns_to_repair = repair_inputs["columns_to_repair"]
        injected = repair_inputs["injected"]
        truth = repair_inputs["truth"]
        labels = repair_inputs["labels"]

        anomaly_array = np.invert(np.isclose(injected, truth)).sum(axis=1)

        n, m = injected.shape
        assert len(anomaly_array) == n

        length = 100
        n_splits = int(n/length)
        print(anomaly_array)
        print(n_splits)
        splits = np.array_split(anomaly_array,n_splits)
        split_indices = np.array_split(np.arange(len(anomaly_array)),n_splits)

        first_anomalous_split = 0
        for i,split in enumerate(splits):
            if np.any(split):
                first_anomalous_split = i # start from here
                break

        split_indices = split_indices[first_anomalous_split:]

        n_splits = len(split_indices)
        index_min = min(split_indices[0])
        self.counter = 0

        for indices in split_indices:
            index_max = max(indices)
            import sys
            injected_part = injected.iloc[index_min:index_max,:].copy()
            truth_part = truth.iloc[index_min:index_max,:].copy()
            labels_part = labels.iloc[index_min:index_max,:].copy()
            def fx(params):
                self.counter += 1
                sys.stdout.write(f"\rhalving search search {self.counter / len(param_combinations) * 100:.1f} %", )
                estim = self.estim_change_copy(params)
                score_ = estim.scores(injected_part,
                                      truth_part,
                                      columns_to_repair,
                                      labels_part,score=self.error_score)[self.error_score]
                return score_
            with Pool(8) as p:
                 scores = np.array(p.map(fx, param_combinations))
                 sorted_indices = np.argsort(np.array(scores))
            scores = [fx(comb)  for comb in param_combinations]
            sorted_indices = np.argsort(np.array(scores))
            #reduce param combinations
            param_combinations = np.array(param_combinations)[sorted_indices[int(len(sorted_indices)/2):]]
            if len(param_combinations) < 5:
                break



        return self.grid(repair_inputs,None ,param_combinations)


    def grid(self, repair_inputs, param_grid, combination_list = None):
        if combination_list is not None:
            param_combinations = combination_list
        else:
            param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
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
