import itertools
from multiprocessing import Pool

import numpy as np

from parameter_search.estimator_optimizer import EstimatorOptimizer

INITIAL_LENGTH = 100



class SuccessiveHalvingOptimizer(EstimatorOptimizer):

    def search(self, repair_inputs, param_grid):
        param_combinations = list(dict(zip(param_grid.keys(), x)) for x in itertools.product(*param_grid.values()))
        columns_to_repair = repair_inputs["columns_to_repair"]
        injected = repair_inputs["injected"]
        truth = repair_inputs["truth"]
        labels = repair_inputs["labels"]

        anomaly_array = np.invert(np.isclose(injected, truth)).sum(axis=1)

        n, m = injected.shape
        assert len(anomaly_array) == n

        length = INITIAL_LENGTH
        n_splits = int( n /length)
        splits = np.array_split(anomaly_array ,n_splits)
        split_indices = np.array_split(np.arange(len(anomaly_array)) ,n_splits)

        first_anomalous_split = 0
        for i ,split in enumerate(splits):
            if np.any(split):
                first_anomalous_split = i # start from here
                break

        split_indices = split_indices[first_anomalous_split:]

        n_splits = len(split_indices)
        index_min = min(split_indices[0])
        self.counter = 0


        for indices in split_indices:
            index_max = max(indices)

            #select data subset
            reduced_repair_indputs = {
                "injected" : injected.iloc[index_min:index_max, :].copy(),
                "truth" : truth.iloc[index_min:index_max, :].copy(),
                "labels" : labels.iloc[index_min:index_max, :].copy(),
                "columns_to_repair" : repair_inputs["columns_to_repair"]
            }

            params_error = self.param_map(reduced_repair_indputs,param_combinations)
            print(params_error)
            # reduce param combinations
            param_combinations =[params for i,(params,_) in enumerate(params_error) if i < len(params_error)/2]

            if len(param_combinations) < 5:
                break

        return self.grid(repair_inputs ,None ,param_combinations)