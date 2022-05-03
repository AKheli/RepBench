from abc import ABC
import pandas as pd
from sklearn.base import BaseEstimator
from Scenarios.metrics import RMSE


class Estimator(ABC, BaseEstimator):

    def __init__(self, columns_to_repair, **kwargs):
        self.columns_to_repair = columns_to_repair
        self.__dict__.update(kwargs)

    # predict , fit and score for the sklearn parameter optizimiters
    def score(self, X, y, columns=None):
        score_ = -RMSE(pd.DataFrame(self.predict(X, y)), pd.DataFrame(y), self.columns_to_repair)
        return score_

    def fit(self, X, y=None):
        raise NotImplementedError(self)

    def predict(self, X, y=None):
        raise NotImplementedError(self)


    def get_params(self, deep= False):
        "needed for training"
        single_params = {"columns_to_repair": self.columns_to_repair}
        single_params.update(self.get_fitted_params())
        return single_params

    def get_fitted_params(self, **args):
        raise NotImplementedError(self)





    def suggest_param_range(self, X):
        "parameter ranges used for training depending on data X"
        raise NotImplementedError(self)

    def get_alg_type(self):
        "e.g for colors in plot"
        raise NotImplementedError(self)

    def algo_name(self):
        raise NotImplementedError(self)

    def __main__(self):
        return self
