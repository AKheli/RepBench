import pandas as pd

from Repair.Screen.screen import screen
from Repair.algorithms_config import SCREEN
from Repair.estimator import Estimator
import numpy as np

class SCREENEstimator(Estimator):

    def __init__(self, t=3, smax=None, smin=None, method="local",**kwargs):
        self.smin = smin
        self.smax = smax
        self.t = t
        self.method = method

    def get_fitted_params(self, **args):
        return {"t": self.t
            , "smin": self.smin
            , "smax": self.smax
            , "method": self.method
        }


    def suggest_param_range(self,X):
        return { "smax" : np.linspace(0.01,2,num = 100),
                "smin" : -np.linspace(0.01,2,num = 100)}


    def repair(self,injected,truth, columns_to_repair , labels=None):
        repair = injected.copy()
        for col in [c for c in columns_to_repair if c < injected.shape[1]]:
            x = np.array(injected.iloc[:, col])

            perc = np.percentile(sorted(np.diff(x)), [2.5, 97.5])
            if self.smax is None:
                smax = perc[1]
                smin = perc[0]
            else:
                smin , smax = self.smin , self.smax
            repair_result = screen(x, self.t , smax, smin)
            repair.iloc[:, col] = repair_result
        return repair

    @property
    def alg_type(self):
        return SCREEN

    def __str__(self):
        return  f'SCREEN({self.t},{round(self.smax,1)},{round(self.smin,1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()