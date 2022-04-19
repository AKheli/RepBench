from abc import ABC

import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
from sklearn.base import BaseEstimator

from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE
from Scenarios.scenario_saver.plotters import generate_repair_plot, generate_correlated_series_plot, \
    generate_truth_and_injected, generate_line_plot, generate_bouneries_plot


class estimator(ABC, BaseEstimator):
    def __init__(self, columns_to_repair, **kwargs):
        self.cols = columns_to_repair
        self.times = {}
        self.times["fit"] = {"total": 0}
        self.times["predict"] = {"total": 0}
        self.to_plot = []
        self.__dict__.update(kwargs)
        self.is_fitted = False
        self.hashed_train = {}
        self.is_training = False

    # predict , fit and score for the sklearn parameter opzimiters
    def predict(self, X ,y=None):
        timer = Timer()
        timer.start()
        result = self._predict(X,y)
        self.times["predict"] = timer.get_time()
        return result

    def fit(self, X, y=None, name=""):
        timer = Timer()
        X = np.array(X)
        result = self._fit(X, y=y)
        self.times["fit"][name] = timer.get_time()
        self.times["fit"]["total"] += timer.get_time()
        return result

    def get_fitted_attributes(self):
        "dict of fitted atributes"
        raise NotImplementedError(self)

    def merge_fitted_attributes(self, list_of_fit_results, anomaly_vector_list=None):
        for l in list_of_fit_results:
            # for key in l.keys():
            #     assert  hasattr(self,key) , key
            pass

    def score(self, X, y):
        score_ = -RMSE(pd.DataFrame(self._predict(X,y)), pd.DataFrame(y), self.cols)
        return score_

    ##evaluation functions
    def error(self, X, y, plt=None, name="", lw=2):
        predicted = pd.DataFrame(self._predict(X))
        original_error = RMSE(X, y, self.cols)
        predicted_error = RMSE(predicted, y, self.cols)
        self.to_plot.append({"injected": X, "original": y, "predicted": predicted, "name": name})

        if plt is not None:
            truth = y
            cols = self.cols
            repair_df = predicted
            generate_correlated_series_plot(truth, cols, lw, ax=plt)
            plt.set_xlim((truth.index[0] - 2, truth.index[-1] + 2))
            generate_repair_plot(repair_df, cols, name, lw, ax=plt)
            plt.set_title(name)
            generate_truth_and_injected(truth, X, cols, lw=2, ax=plt)
            plt.xaxis.set_major_locator(MaxNLocator(integer=True))

            generate_bouneries_plot(self.lower, self.upper, lw, ax=plt)
            generate_line_plot(self.reduced, lw, ax=plt)

        return {"original_error": original_error, "error": predicted_error, "ratio": predicted_error / original_error}

    def _predict(self, X , y = None):
        raise NotImplementedError(self)

    def _fit(self, X, y=None):
        raise NotImplementedError(self)

    def suggest_param_range(self, X):
        raise NotImplementedError(self)

    def train(self, X, y):
        self.is_training = True

        hash_ = hash(str(X) + str(y))

        if hash_ in self.hashed_train:
            self.__dict__.update(self.hashed_train[hash_])
        else:
            opt = BayesianOptimization(self, self.suggest_param_range(X), n_jobs=1)
            opt.fit(X, y)
            fitted_attr = opt.best_estimator_.get_params()
            self.__dict__.update(fitted_attr)
            self.hashed_train[hash_] = fitted_attr.copy()
            print(self.get_fitted_attributes())

        assert self.is_training

        self.is_training = False

    def repair(self, X ,y = None):
        timer = Timer()
        timer.start()
        repair = self.predict(X,y)
        return {"repair": pd.DataFrame(repair)
            , "runtime": timer.get_time()
            , "type": self.alg_type
            , "name": self.algo_name()
            , "params": self.get_params()
                }

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