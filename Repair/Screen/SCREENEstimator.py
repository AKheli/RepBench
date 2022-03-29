import pandas as pd

from Repair.Algorithms_File import SCREEN
from Repair.Screen.Local import screen
from Repair.estimator import estimator
import numpy as np


alg_type = SCREEN
class SCREEN_estimator(estimator):

    def __init__(self, t=3, smax=1, smin=-1, method="local",**kwargs):
        self.smin = smin
        self.smax = smax
        self.t = t
        self.alg_type = alg_type
        self.method = method
        assert self.smin < 0 and self.smax > 0 and t >= 1 , f"{(smin,smax,t)}"
        estimator.__init__(self,**kwargs)


    def get_params(self, **kwargs):
        return {"t": self.t
            , "smin": self.smin
            , "smax": self.smax
            , "method": self.method
        }


    def suggest_param_range(self,X):
        differences = abs(np.diff(X.values))
        #todo smin and smax suggestion
        return {"t" : list(range(15)) ,
                "smax" : np.linspace(min(differences),max(differences),num = 100),
                "smin" : np.linspace(min(differences),max(differences),num = 100)}



    def _fit(self, X, y=None): ## no fitting
        if isinstance(X,pd.DataFrame):
            X = X.values
            y = y.values

        X_bar = np.mean(X,axis=1)
        y_bar = np.mean(y,axis=1)
        non_anom = np.isclose(X_bar,y_bar)
        diff = np.diff(X_bar[non_anom])
        self.smin = min(diff)
        self.smax =  max(diff)
        self.is_fitted = True
        return self

    def _predict(self, X):
        repair = X.copy()
        for col in [c for c in self.cols if c < X.shape[1]]:
            x = np.array(X.iloc[:, col])
            repair_results = screen(x, SMIN=self.smin, SMAX=self.smax, T=self.t)
            repair.iloc[:, col] = repair_results["repair"]

        return repair

    def __main__(self):
        return self


    def algo_name(self):
        # todo with different train we get different best values
        return  f'SCREEN' #({self.t},{round(self.smax,1)},{round(self.smin,1)})'
