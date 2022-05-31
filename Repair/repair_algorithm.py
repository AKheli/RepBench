import itertools

import numpy as np
import pandas as pd
import sklearn.metrics as sm
from skopt import gp_minimize

from Repair.estimator_optimizer import  EstimatorOptimizer
import Repair.algorithms_config as ac
from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.Dimensionality_Reduction.CD.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Repair.estimator import Estimator
from Repair.res.timer import Timer

class RepairAlgorithm:
    repair_estimators = {"rpca": Robust_PCA_estimator, "screen": SCREEN_estimator, "cdrec": CD_Rec_estimator,
                         "imr": IMR_estimator}

    def __init__(self, estimator_name, columns_to_repair, **kwargs):
        estimator = None
        self.estimator_name = None

        # checks if specian name is given to algorithm , for example with toml params
        if "name" in kwargs:
            self.type = kwargs["name"]
            assert isinstance(self.type, str)
            kwargs.pop("name")

        ### parse alg
        if estimator_name in (ac.IMR, "imr"):
            estimator = IMR_estimator(columns_to_repair=columns_to_repair, **kwargs)
        if estimator_name in (ac.SCREEN, "screen"):
            estimator = SCREEN_estimator(columns_to_repair=columns_to_repair, **kwargs)
        if estimator_name in (ac.RPCA, "rpca"):
            estimator = Robust_PCA_estimator(columns_to_repair=columns_to_repair, **kwargs)
        if estimator_name in (ac.CDREC, "cdrec"):
            estimator = CD_Rec_estimator(columns_to_repair=columns_to_repair, **kwargs)
        assert estimator is not None, f'{estimator_name} could not be parsed'

        self.estimator: Estimator = estimator
        self.columns_to_repair_ = columns_to_repair

        self._hashed_train_ = {}
        self.times = {}
        self.times["fit"] = {"total": 0}
        self.times["predict"] = {"total": 0}
        self.train_results = {}

    @property
    def columns_to_repair(self):
        return self.columns_to_repair_

    @columns_to_repair.setter
    def columns_to_repair(self, val):
        # assert isinstance(val,list) , "columns must be a list even when a single collumn is used"
        self.estimator.columns_to_repair = val
        self.columns_to_repair_ = val

    # ##evaluation functions
    # def error(self, X, y):
    #     predicted = pd.DataFrame(self.estimator.predict(X))
    #     original_error = RMSE(X, y, self.columns_to_repair)
    #     predicted_error = RMSE(predicted, y, self.columns_to_repair)
    #     return {"original_error": original_error, "error": predicted_error,
    #             "ratio": predicted_error / original_error}


    def train(self, * ,injected, truth,injected_columns,labels , error_score, train_method, **kwargs):

        self.estimator.columns_to_repair = injected_columns
        if True: # hash_ not in self.train_results:
            assert injected.shape[1] >2

            print("training", self.estimator.alg_type)
            print("train size:", injected.shape)

            param_grid = self.estimator.suggest_param_range(injected)
            estimator_optimizer = EstimatorOptimizer(self.estimator,train_method, error_score)



            optimal_params = estimator_optimizer.find_optimal_params(injected,truth,labels,param_grid)
            assert all([ k in param_grid.keys() for k in optimal_params.keys()])
            #self.train_results[hash_] = optimal_params

        self.estimator.__dict__.update(optimal_params)

        return optimal_params

    def repair(self, injected, injected_columns, truth, labels , **kwargs):
        self.estimator.columns_to_repair = injected_columns
        attributes_str = str(self.estimator.get_params())
        timer = Timer()
        timer.start()
        repair = self.estimator.predict(injected, truth, labels=labels)
        scores = self.estimator.scores(injected,truth,labels=labels,predicted=repair)
        repair = pd.DataFrame(repair)

        assert attributes_str == str(
            self.estimator.get_params()), f'{attributes_str} \n {str(self.estimator.get_params())}'

        retval = {"repair": repair
            , "runtime": timer.get_time()
            , "type": self.estimator.alg_type
            , "name": str(self.estimator) if self.estimator_name is None else self.estimator_name
            , "params": self.estimator.get_fitted_params()
            , "scores" : scores
            }
        return retval

    @property
    def alg_type(self):
        return self.estimator.alg_type

    def __repr__(self):
        return self.estimator.__str__()

    def set_params(self,params):
        self.estimator.__dict__.update(params)