import time

import numpy as np
from pandas import DataFrame

from Injection.injected_data_part import InjectedDataContainer
from algorithms.Dimensionality_Reduction.dimensionality_Reduction_estimator import DimensionalityReductionEstimator
from algorithms.algorithm_mapper import algo_mapper
from algorithms.estimator import Estimator
from algorithms import algorithms_config as alg_config

def shuffle_labels(labels: DataFrame):
    for i, _ in enumerate(labels):
        np.random.shuffle(labels.iloc[:, i].values)
    return labels


class AnomalyRepairer():
    def __init__(self, runtime_measurements=1, label_resample=0):
        self.runtime_measurements = runtime_measurements
        self.label_randomizer = label_resample

    def repair(self, alg_type, params="default", *, columns_to_repair, injected, truth=None, labels=None):
        """
            Parameters
            ----------
            alg_type : str
            injected :  anomalous df
            truth : truth df
            labels : boolean labels used for IMR

             Parameters
            ----------
            dict : { repair : df , runtime :str , scores : dict }
            """

        if params == "default":
            params = {}
        assert isinstance(params, dict), f"params must be a dictionary or 'default', was {params}"

        estimator: Estimator = algo_mapper[alg_type](**params)
        used_labels = estimator.uses_labels
        if used_labels:
            assert truth is not None and labels is not None, "this algorithm requires labeled truth values"

        start = time.time()

        score_list = []
        for i in range(max(1, self.runtime_measurements, self.label_randomizer)):
            repair = estimator.repair(truth=truth, injected=injected, columns_to_repair=columns_to_repair,
                                      labels=labels)
            scores = estimator.scores(injected, truth, columns_to_repair, labels, predicted=repair)
            score_list.append(scores)
            if i >= self.runtime_measurements - 1 and not used_labels:
                break
            # labels = shuffle_labels(labels)

        end = time.time()

        runtime = (end - start) / self.runtime_measurements

        retval = {
            "repair": repair,
            "runtime": runtime,
            "scores": scores,
            "params": estimator.get_fitted_params()
        }
        return retval

    def repair_data_part(self, alg_type, data_part: InjectedDataContainer, params="default", add_repair=True , additional_context=False):
        if additional_context:
            try:
                retval = self.repair_with_additonal_context(alg_type, params=params, **data_part.repair_inputs)
            except Exception as e:
                print(alg_type + " on " + str(data_part))
                raise e
            data_part.add_repair(retval, alg_type)
            return retval

        else:
            try:
                retval = self.repair(alg_type, params=params, **data_part.repair_inputs)
            except Exception as e:
                print(alg_type + " on " + str(data_part))
                raise e
            data_part.add_repair(retval, alg_type)
            return retval



    def repair_with_additonal_context(self, alg_type, params="default", *, columns_to_repair, injected, truth=None, labels=None):
        if params == "default":
            params = {}
        assert isinstance(params, dict), f"params must be a dictionary or 'default', was {params}"

        estimator: Estimator = algo_mapper[alg_type](**params)
        used_labels = estimator.uses_labels
        if used_labels:
            assert truth is not None and labels is not None, "this algorithm requires labeled truth values"

        start = time.time()

        score_list = []
        for i in range(max(1, self.runtime_measurements, self.label_randomizer)):
            repair = estimator.repair(truth=truth, injected=injected, columns_to_repair=columns_to_repair,
                                      labels=labels)
            scores = estimator.scores(injected, truth, columns_to_repair, labels, predicted=repair)
            score_list.append(scores)
            if i >= self.runtime_measurements - 1 and not used_labels:
                break
            # labels = shuffle_labels(labels)

        end = time.time()

        runtime = (end - start) / self.runtime_measurements

        retval = {
            "repair": repair,
            "runtime": runtime,
            "scores": scores,
            "params": estimator.get_fitted_params()
        }

        additional_results = {}

        if alg_type in [alg_config.Robust_PCA,alg_config.CDREC]:
            estimator : DimensionalityReductionEstimator
            additional_results["weights"] = estimator.weights_i_["classify"]
            additional_results["reduced"] = estimator.reduced_i_["classify"]
            additional_results["reduced_repair"] = estimator.reduced_i_["classify"]
        retval["additional_results"] = additional_results

        return retval
