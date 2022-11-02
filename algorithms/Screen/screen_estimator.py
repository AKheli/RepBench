import pandas as pd

from algorithms.Screen.globallp import LPconstrainedAE
from algorithms.Screen.screen import screen
from algorithms.algorithms_config import SCREEN, SCREEN_GLOBAL
from algorithms.estimator import Estimator
import numpy as np


class SCREENEstimator(Estimator):

    def __init__(self, t:int=3, smax: float = 0.1, smin :float =0.2, method : str ="local", ci=None ,**kwargs):
        """
        param ci need to be a tuple e.g (0.1,0.9)
        """
        self.smin = smin
        self.smax = smax
        self.t = t
        self.method = method
        self.ci = ci

    def get_fitted_params(self, **args):
        return {"t": self.t
            , "smin": self.smin
            , "smax": self.smax
            , "method": self.method
                }

    def suggest_param_range(self, X):
        return {"smax": np.linspace(0.01, 2, num=100),
                "smin": -np.linspace(0.01, 2, num=100)}

    def repair(self, injected, truth, columns_to_repair, labels=None):
        repair = injected.copy()

        columns_to_repair = [c for c in columns_to_repair if c < injected.shape[1]]
        for col in columns_to_repair:
            x = np.array(injected.iloc[:, col])

            if self.ci is not None:
                self.ci =  (self.ci[0] if self.ci[0]>1 else self.ci[0]*100 ,
                            self.ci[1] if self.ci[1]>1 else self.ci[1]*100 )
                perc = np.percentile(sorted(np.diff(x)), tuple(self.ci))
                smax = perc[1]
                smin = perc[0]
                print("smin",smin)
                print("smax",smax)
                print(perc)
                print(tuple(self.ci))
                print(sorted(abs(np.diff(x))))
                self.smax = smax
                self.smin = smin
            else:
                smin, smax = self.smin, self.smax
            if self.method == "local":
                repair_result = screen(x, self.t, smax, smin)
            if self.method == "global":
                repair_result = LPconstrainedAE(x, smax, -smin, w=self.t)
            repair.iloc[:, col] = repair_result
        return repair

    @property
    def alg_type(self):
        return SCREEN_GLOBAL if self.method == "global" else SCREEN

    def __str__(self):
        return f'SCREEN({self.t},{round(self.smax, 1)},{round(self.smin, 1)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()
