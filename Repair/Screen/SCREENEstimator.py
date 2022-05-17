import pandas as pd

from Repair.Screen.screen import screen
from Repair.algorithms_config import SCREEN
from Repair.estimator import Estimator
import numpy as np


alg_type = SCREEN
class SCREEN_estimator(Estimator):

    def __init__(self, t=3, smax=1, smin=-1, method="local",**kwargs):
        self.smin = smin
        self.smax = smax
        self.t = t
        self.alg_type = alg_type
        self.method = method
        assert self.smin < 0 and self.smax > 0 and t >= 1 , f"invalid (smin<0,smax>0,t>=1): {(smin,smax,t)}"

        Estimator.__init__(self,**kwargs)

    def get_fitted_params(self, **args):
        return {"t": self.t
            , "smin": self.smin
            , "smax": self.smax
            , "method": self.method
        }


    def suggest_param_range(self,X):
        differences = abs(np.diff(X.values))
        #todo smin and smax suggestion
        return { "smax" : np.logspace(-3,0,num = 10),
                "smin" : -np.logspace(-3,0,num = 10)}



    def fit(self, X, y=None): ## no fitting
        self.is_fitted = True
        return self

    def predict(self, X , y = None,labels=None):
        repair = X.copy()
        for col in [c for c in self.columns_to_repair if c < X.shape[1]]:
            x = np.array(X.iloc[:, col])
            repair_result = screen(x, self.t , self.smax , self.smin)
            repair.iloc[:, col] = repair_result

        return repair

    def alg_type(self):
        return "SCREEN"

    def __str__(self):
        return  f'SCREEN({self.t},{round(self.smax,1)},{round(self.smin,1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()