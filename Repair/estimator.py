from abc import ABC

import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
from sklearn.base import BaseEstimator

from Repair.res.timer import Timer
from Scenarios.metrics import RMSE
from Scenarios.scenario_saver.plotters import generate_repair_plot, generate_correlated_series_plot, \
    generate_truth_and_injected, generate_line_plot, generate_bouneries_plot


class estimator(ABC,BaseEstimator):
    def __init__(self,**kwargs):
        self.times = {}
        self.times["fit"] = {"total" : 0}
        self.times["predict"] = {"total" : 0}
        self.to_plot = []
        self.window_size = "full"
        self.anomaly_col_dict = {}
        self.__dict__.update(kwargs)



    #predict , fit and score for the sklearn parameter opzimiters
    def predict(self,X, name = ""):
        timer = Timer()
        timer.start()
        result = self._predict(X)
        self.times["predict"]["total"] += timer.get_time()
        return result



    def fit(self,X,y=None , name = ""):
        X = np.array(X)
        if y is not None:
            y = np.array(y)
            for i in self.cols:
                col_dif = np.array(X[:,i]) - np.array(y[:,i])
                self.anomaly_col_dict[i] = np.abs(col_dif) > 0.0000001

        if self.window_size == "full":
            timer = Timer()
            timer.start()
            result = self._fit(X, y=y)
            self.times["fit"][name] =  timer.get_time()
            self.times["fit"]["total"] += timer.get_time()
            return result

        ts_length = X.shape[0]
        assert ts_length > 40 #todo delete

        # #windowed fit
        # if ts_length < self.window_size:
        #     self.window_size = ts_length
        #
        # s = list(np.arange(0, ts_length, step=self.window_size))
        #
        # if len(s)>1:
        #     s[-1] = ts_length - 1
        # else:
        #     s.append(ts_length-1)
        #
        #
        # assert s[0] == 0 and s[-1] == ts_length-1 , (s[0] , s[-1] , s, ts_length)
        #
        # fitted_atributes = []
        # anomaly_vec = []
        # for start, stop in zip(s[:-1],s[1:]):
        #     if y is not None:
        #         self._fit(X[start:stop,:], y[start:stop,:])
        #         fitted_atributes.append(self.get_fitted_attributes())
        #         anomaly_vec.append(np.logical_or.reduce([*self.anomaly_col_dict.values()]))
        #
        #     else :
        #         self._fit(X[start:stop, :])
        #         fitted_atributes.append(self.get_fitted_attributes())
        #
        # self.merge_fitted_attributes(fitted_atributes,anomaly_vec if len(anomaly_vec) > 0 else None)

        return self

    def get_fitted_attributes(self):
        "dict of fitted atributes"
        raise NotImplementedError

    def merge_fitted_attributes(self, list_of_fit_results,anomaly_vector_list = None):
        for l in list_of_fit_results:
            # for key in l.keys():
            #     assert  hasattr(self,key) , key
            pass


    def score(self,X,y):
        score_ = -RMSE(pd.DataFrame(self._predict(X)),pd.DataFrame(y),self.cols)
        return score_


    ##evaluation functions
    def error(self,X,y ,  plt = None , name ="" , lw = 2):
        predicted = pd.DataFrame(self._predict(X))
        original_error = RMSE(X, y, self.cols)
        predicted_error = RMSE(predicted, y, self.cols)
        self.to_plot.append({"injected" : X, "original" : y , "predicted" : predicted , "name" : name})

        if plt is not None:
            truth = y
            cols = self.cols
            repair_df = predicted
            generate_correlated_series_plot(truth, cols, lw ,ax=plt)
            plt.set_xlim((truth.index[0] - 2, truth.index[-1] + 2))
            generate_repair_plot(repair_df, cols, name, lw,ax=plt)
            plt.set_title(name)
            generate_truth_and_injected(truth, X, cols, lw = 2,ax=plt)
            plt.xaxis.set_major_locator(MaxNLocator(integer=True))

            # try:
            #self.reduced.plot(title = "reduced")
            generate_bouneries_plot(self.lower,self.upper,lw,ax=plt)
            generate_line_plot(self.reduced,lw,ax=plt)
            #generate_line_plot(self.pca,lw,ax=plt , color = "yellow")

            # except:
            #     assert False
            #     pass

        return {"original_error" : original_error , "error" : predicted_error , "ratio" : predicted_error/original_error}



    def _predict(self, X):
        raise NotImplementedError

    def _fit(self, X, y=None):
        raise NotImplementedError

