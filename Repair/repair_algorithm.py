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
from Repair.train_call_back import train_call_back
from Scenarios.metrics import RMSE
import sklearn.model_selection as sk_ms


class RepairAlgorithm:
    optimizer = "bayesian"

    repair_estimators = {"rpca": Robust_PCA_estimator, "screen": SCREEN_estimator, "cdrec": CD_Rec_estimator,
                         "imr": IMR_estimator}

    def __init__(self, estimator_name, columns_to_repair, **kwargs):
        estimator = None
        self.type = None

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

    ##evaluation functions
    def error(self, X, y):
        predicted = pd.DataFrame(self.estimator.predict(X))
        original_error = RMSE(X, y, self.columns_to_repair)
        predicted_error = RMSE(predicted, y, self.columns_to_repair)
        return {"original_error": original_error, "error": predicted_error,
                "ratio": predicted_error / original_error}

    def normalize(self, X):
        """
        Parameters: matrix X
        Returns: normalized X , normalization_inverse function
        """
        mean_X, std_X = X.mean(), X.std()
        assert (len(mean_X), len(std_X)) == (X.shape[1], X.shape[1])

        def inv_func(X_norm):
            X_norm.columns = X.columns
            result = X_norm * std_X + mean_X
            return result

        return (X - mean_X) / std_X, inv_func



    def train(self, injected, truth,injected_columns,labels, score_indices, **kwargs):
        self.estimator.columns_to_repair = injected_columns
        self.estimator.set_train_call_back(train_call_back(labels, score_indices))

        X, inv = self.normalize(injected)


        hash_ =hash((str(injected.values),str(truth.values),str(injected_columns),str(labels)))
        if hash_ not in self.train_results:
            assert X.shape[1] >2

            y, _ = self.normalize(truth)

            print("training", self.get_type())
            print("train size:", X.shape)

            param_grid = self.estimator.suggest_param_range(X)
            estimator_optimizer = EstimatorOptimizer(self.estimator,self.optimizer)
            optimal_params = estimator_optimizer.find_optimal_params(X,y,labels,param_grid)
            assert all([ k in param_grid.keys() for k in optimal_params.keys()])
            self.train_results[hash_] = optimal_params

        self.estimator.__dict__.update(self.train_results[hash_])
        return

    def repair(self, injected, injected_columns, truth, labels , **kwargs):
        self.estimator.columns_to_repair = injected_columns
        attributes_str = str(self.estimator.get_params())

        X, X_norn_inv = self.normalize(injected)
        y, _ = self.normalize(truth)
        timer = Timer()
        timer.start()
        assert labels is not None
        repair = self.estimator.predict(X, y, labels=labels)
        repair = pd.DataFrame(repair)  # *std_X+mean_X
        repair = X_norn_inv(repair)

        assert attributes_str == str(
            self.estimator.get_params()), f'{attributes_str} \n {str(self.estimator.get_params())}'
        return {"repair": repair
            , "runtime": timer.get_time()
            , "type": self.get_type()
            , "name": str(self.estimator)
            , "params": self.estimator.get_fitted_params()
                }

    def get_type(self):
        return self.type if self.type is not None else self.estimator.alg_type
    def __repr__(self):
        return self.estimator.__str__()
