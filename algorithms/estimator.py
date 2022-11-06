from abc import ABC
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import sklearn.metrics as sm


class Estimator(ABC, BaseEstimator):
    uses_labels = False

    def copy(self):
        copy_ = type(self)
        copy_.score_f = self.score_f
        return copy_

    def set_score_f(self,score):
        self.score_f = score

    def scores(self, injected, truth , columns_to_repair, labels ,*, predicted=None , score = None):
        """
        :param injected: injected data
        :param truth: original data
        :param columns_to_repair: columns to repair
        :param labels: labels of known ground truth as used by the IMR algorithm
        that are excluded form the error computation
        :param predicted: predicted data if none repair is called
        :param score: score if none a dictiornary with mae,rmse,partial_rmse is returned

        :return: score or dict with scores
        """
        if predicted is None:
            predicted = self.repair(X, y,columns_to_repair,labels).values

        labels = labels.values if isinstance(labels,pd.DataFrame) else labels
        X = injected.values if isinstance(injected,pd.DataFrame) else injected
        y = truth.values if isinstance(truth,pd.DataFrame) else truth
        predicted = predicted.values if isinstance(predicted,pd.DataFrame) else predicted

        non_labeled = np.invert(labels.astype(bool))
        partial_weights = np.logical_and(np.invert(np.isclose(X, y)), non_labeled)


        mae = 0
        mse = 0
        original_mse = 0
        partial_mse = 0
        rmse_per_col = []
        for col in columns_to_repair:
            print(non_labeled)
            print(y)
            print(non_labeled)
            print(y[non_labeled[:,col],col])
            mae += sm.mean_absolute_error(y[non_labeled[:,col],col], predicted[non_labeled[:,col],col])
            mse_col = sm.mean_squared_error(y[non_labeled[:,col],col],predicted[non_labeled[:,col],col])
            mse += mse_col
            rmse_per_col.append((col, np.sqrt(mse_col)))
            partial_mse += sm.mean_squared_error(y[partial_weights[:,col],col], predicted[partial_weights[:,col],col])
            original_mse += sm.mean_squared_error(y[:,col], X[:,col])

        scores = {}
        scores['mae'] = mae
        scores['rmse'] = np.sqrt(mse)
        scores['partial_rmse'] = np.sqrt(partial_mse)
        scores['rmse_per_col'] = rmse_per_col
        scores['original_rmse'] = np.sqrt(original_mse)


        if score is not None:
            return scores[score]
        else:
            return scores


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


    def repair(self,injected, truth, columns_to_repair , labels=None):
        raise NotImplementedError(self)

    def get_params(self, deep= False):
        return self.get_fitted_params()

    def get_fitted_params(self, **args):
        raise NotImplementedError(self)

    def suggest_param_range(self, X):
        "parameter ranges used for training depending on data X, data is normalized for training"
        raise NotImplementedError(self)


    @property
    def alg_type(self):
        "e.g. for colors in plot"
        raise NotImplementedError(self)

    def algo_name(self):
        raise NotImplementedError(self)

    def addiotnal_plotting_args(self) -> dict:
        # col_index :  kwargs for plt.plot()
        return {}



