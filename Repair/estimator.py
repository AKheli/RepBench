from abc import ABC

import numpy as np
from sklearn.base import BaseEstimator
import sklearn.metrics as sm


class Estimator(ABC, BaseEstimator):

    def __init__(self, columns_to_repair,train_call_back = None):
        self.columns_to_repair = columns_to_repair
        self.train_call_back = train_call_back
        self.score_f = "full_rmse"


    def copy(self):
        copy_ =  type(self)(self.columns_to_repair)
        copy_.score_f = self.score_f
        return copy_

    def set_score_f(self,score):
        self.score_f = score

    def set_train_call_back(self,train_call_back):
        self.train_call_back = train_call_back



    def score(self, X, y , labels):
        """ error_to_maximize """
        score_ = None
        if self.score_f == "full_rmse":
            score_ = -self.full_rmse(X,y,labels)

        if self.score_f == "partial_rmse":
            score_ = -self.partial_rmse(X, y, labels)

        if self.score_f == "mae":
            score_ = -self.mae_score(X, y, labels)

        # if self.score_f == "mutual_info":
        #     score_ = sm.normalized_mutual_info_score( flatten_y,flatten_predicted)
        #     print("mutual_info" ,score_)

        assert score_ is not None , f"score_f must be: mutual_info, mae , partial_rmse or full_rmse"
        return score_

    def mae_score(self, X, y , labels):
        predicted = self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.ones_like(predicted.values).astype(bool)
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_absolute_error(flatten_y[weights], flatten_predicted[weights])
        return score_

    def full_rmse(self, X, y, labels):
        predicted  =self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.ones_like(predicted.values).astype(bool)
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_squared_error(flatten_y[weights], flatten_predicted[weights],squared=False)
        return score_


    def partial_rmse(self, X, y, labels):
        predicted = self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.invert(np.isclose(X.values,y.values))
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_squared_error(flatten_y[weights], flatten_predicted[weights],squared=False)
        return score_


    def fit(self, X, y=None):
        raise NotImplementedError(self)

    def predict(self, X, y=None , labels=None):
        """ injected dataframe X
            truth data frame y
            labeld points labels
            returns  repaired dataframe
        """
        raise NotImplementedError(self)


    def get_params(self, deep= False):
        """
        returns all attributes that are needed for the sk optimize library
        """
        fix_params = {
            "columns_to_repair": self.columns_to_repair,
            "train_call_back" : self.train_call_back,
        }
        fix_params.update(self.get_fitted_params())
        return fix_params

    def get_fitted_params(self, **args):
        raise NotImplementedError(self)

    def suggest_param_range(self, X):
        "parameter ranges used for training depending on data X, data is normalited for training"
        raise NotImplementedError(self)

    def get_alg_type(self):
        "e.g for colors in plot"
        raise NotImplementedError(self)

    def algo_name(self):
        raise NotImplementedError(self)

    def __main__(self):
        return self
