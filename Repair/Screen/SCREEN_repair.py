import numpy as np
from sklearn.base import BaseEstimator

from Repair.Algorithms_File import SCREEN, ALGORITHM_PARAMETERS
from Repair.Screen.Local import screen
from Repair.res.timer import Timer

alg_type = SCREEN
default_params = ALGORITHM_PARAMETERS[alg_type]


def SCREEN_repair(injected, cols=[0], params={}, **kwargs):
    SMIN = params.get("smin", default_params["smin"])
    SMAX = params.get("smax", default_params["smax"])
    T = params.get("T", default_params["T"])

    repair = injected.copy()
    timer = Timer()
    for col in cols:
        x = np.array(injected.iloc[:, col])
        timer.start()
        repair_results = screen(x, SMIN=SMIN, SMAX=SMAX, T=T)
        timer.pause()
        repair.iloc[:, col] = repair_results["repair"]

    return {"repair": repair, "runtime": timer.get_time(), "type": alg_type, "name": f'SCREEN({T},{SMAX})'}


class SCREEN_estimator(BaseEstimator):

    def __init__(self, cols=[0], T=1, s=1):
        self.cols = cols
        self.T = T
        self.s = s

    def get_params(self, **kwargs):
        return {"T": self.T,
                "s": self.s
                }

    def fit(self, X, y=None):
        # nothing to fit
        return self

    def predict(self, X):
        repair =  X.copy()
        for col in self.cols:
            x = np.array(X.iloc[:, col])
            repair_results = screen(x, SMIN=-self.s, SMAX=self.s, T=self.T)
            repair.iloc[:, col] = repair_results["repair"]
        return repair

    def __main__(self):
        return self

