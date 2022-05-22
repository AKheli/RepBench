from abc import ABC
from sklearn.base import BaseEstimator
import sklearn.metrics as sm


class Estimator(ABC, BaseEstimator):

    def __init__(self, columns_to_repair,train_call_back = None):
        self.columns_to_repair = columns_to_repair
        self.train_call_back = train_call_back


    def set_train_call_back(self,train_call_back):
        self.train_call_back = train_call_back

    def score(self, X, y , labels):
        """ neg rmse (to maximize) """
        predicted  =self.predict(X, y, labels)
        weights = X.ne(y).values.astype(int)
        weights = weights*3+1 #weights anomalies more
        weights[labels] = 0
        weights = weights.flatten()
        flatten_predicted = predicted.values.flatten()
        flatten_y =  y.values.flatten()
        score_ = -sm.mean_squared_error( flatten_y,flatten_predicted , sample_weight=weights)
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
            "train_call_back" : self.train_call_back
        }
        fix_params.update(self.get_fitted_params())
        return fix_params

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
