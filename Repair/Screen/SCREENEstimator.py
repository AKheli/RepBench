from Repair.Algorithms_File import SCREEN
from Repair.Screen.Local import screen
from Repair.estimator import estimator
import numpy as np


alg_type = SCREEN
class SCREEN_estimator(estimator):

    def __init__(self, t=1, smax=2, smin=None, method="local",**kwargs):
        self.smin = -smax if smin is None else smin
        self.smax = smax
        self.t = int(t)
        self.alg_type = alg_type
        self.method = method

        assert self.smin < 0 and self.smax > 0 and t >= 1
        estimator.__init__(self,**kwargs)


    def get_params(self, **kwargs):
        return {"t": self.t
            , "smin": self.smin
            , "smax": self.smax
            , "type": self.type
        }

    def _fit(self, X, Y=None): ## no fitting
        self.is_fitted = True
        return self

    def _predict(self, X):
        repair = X.copy()
        for col in self.cols:
            x = np.array(X.iloc[:, col])
            repair_results = screen(x, SMIN=self.smin, SMAX=self.smax, T=self.t)
            repair.iloc[:, col] = repair_results["repair"]

        return repair

    def __main__(self):
        return self


    def algo_name(self):
        return  f'SCREEN({self.t},{self.smax})'
