from abc import ABC

import pandas as pd
from matplotlib.ticker import MaxNLocator
from sklearn.base import BaseEstimator

from Repair.res.timer import Timer
from Scenarios.metrics import RMSE
from Scenarios.scenario_saver.plotters import generate_repair_plot, generate_correlated_series_plot, \
    generate_truth_and_injected, generate_line_plot, generate_bouneries_plot


class estimator(ABC,BaseEstimator):
    def __init__(self):
        self.times = {}
        self.times["fit"] = {"total" : 0}
        self.times["predict"] = {"total" : 0}
        self.to_plot = []

    #predict , fit and score for the sklearn parameter opzimiters
    def predict(self,X, name = ""):
        timer = Timer()
        timer.start()
        result = self._predict(X)
        self.times["predict"]["total"] += timer.get_time()
        return result

    def fit(self,X,y=None , name = ""):
        timer = Timer()
        timer.start()
        result = self._fit(X, y=y)
        self.times["fit"][name] =  timer.get_time()
        self.times["fit"]["total"] += timer.get_time()
        return result

    def score(self,X,y):
        return -RMSE(pd.DataFrame(self._predict(X)),y,self.cols)


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

