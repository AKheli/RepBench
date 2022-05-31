from abc import ABC

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import sklearn.metrics as sm


class Estimator(ABC, BaseEstimator):

    def __init__(self, columns_to_repair,train_call_back = None):
        self.columns_to_repair = columns_to_repair
        self.train_call_back = train_call_back

    def copy(self):
        copy_ =  type(self)(self.columns_to_repair)
        copy_.score_f = self.score_f
        return copy_

    def set_score_f(self,score):
        self.score_f = score

    def set_train_call_back(self,train_call_back):
        self.train_call_back = train_call_back



    def scores(self, X, y , labels , predicted=None):

        hash_X = hash(str(X))
        predicted = predicted if predicted is not None else self.predict(X, y, labels)
        labels = labels.values if isinstance(labels,pd.DataFrame) else labels

        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        full_weights = np.ones_like(predicted.values).astype(bool)
        full_weights[labels] = False
        full_weights_flattened = full_weights.flatten()

        scores_ = {}
        scores_["mae"] = sm.mean_absolute_error(flatten_y[full_weights_flattened], flatten_predicted[full_weights_flattened])
        scores_["full_rmse"] = sm.mean_squared_error(flatten_y[full_weights_flattened], flatten_predicted[full_weights_flattened],squared=False)

        partial_weights = np.invert(np.isclose(X.values, y.values))
        partial_weights[labels] = False
        partial_weights_flattened = partial_weights.flatten() # anomaly_weights

        scores_["partial_rmse"] = sm.mean_squared_error(flatten_y[partial_weights_flattened], flatten_predicted[partial_weights_flattened], squared=False)


        ### additional scores
        partial_weights = np.invert(partial_weights)
        partial_weights[labels] = False
        partial_weights_flattened = partial_weights.flatten()
        scores_["N_partial_rmse"] = sm.mean_squared_error(flatten_y[partial_weights_flattened], flatten_predicted[partial_weights_flattened],squared=False)

        scores_["diff_rmse"] = scores_["full_rmse"] - scores_["partial_rmse"]

        assert hash(str(X)) == hash_X
        return scores_

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
        """
        Parameters
        ----------
        X: anomaly matrix
        y: truth values
        labels: indexes assumed to be known

        Returns
        -------
        repaired dataframe
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

    @property
    def alg_type(self):
        "e.g for colors in plot"
        raise NotImplementedError(self)

    def algo_name(self):
        raise NotImplementedError(self)

    def __main__(self):
        return self
