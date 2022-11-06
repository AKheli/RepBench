import time

import numpy as np
from pandas import DataFrame

from Injection.injected_data_part import InjectedDataContainer
from algorithms.algorithm_mapper import algo_mapper
from algorithms.estimator import Estimator


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

        # avg_scores = {}
        # for k, v in scores.items():
        #     if isinstance(v, list): # tuples (ts_col, score)
        #         list_of_score_lists = [score[k] for score in score_list]
        #         n = [(ts,0) for ts,val in list_of_score_lists[0]]
        #         for score_list in list_of_score_lists:
        #             for i,j in enumerate(score_list):
        #                 assert n[i][0] == j[0], f"ts columns must be the same {n[i]} != {j}"
        #                 n[i] = (n[i][0],n[i][1] + j[1]/len(list_of_score_lists) )
        #         avg_scores[k] = n
        #     else:
        #         print("v",v)
        #         print("k",k)
        #         avg_scores[k] = sum([score[k] for score in score_list]) / len(score_list)
        #         avg_scores[k] = sum([d[k] for d in score_list]) / len(score_list)

        retval = {
            "repair": repair,
            "runtime": runtime,
            "scores": scores,
            "params": estimator.get_fitted_params()
        }
        return retval

    def repair_data_part(self, alg_type, data_part: InjectedDataContainer, params="default", add_repair=True):
        try:
            retval = self.repair(alg_type, params=params, **data_part.repair_inputs)
        except Exception as e:
            print(alg_type + " on " + str(data_part))
            raise e
        data_part.add_repair(retval, alg_type)
        return retval
