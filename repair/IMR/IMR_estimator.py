from repair.algorithms_config import IMR
from repair.IMR.IMR import imr
from repair.estimator import Estimator
import numpy as np

class IMR_estimator(Estimator):
    def __init__(self, p=2,tau = 0.037 ,n_max_itr=10000, **kwargs):
        self.p = p
        self.tau = tau
        self.max_itr_n  = n_max_itr

    def get_fitted_params(self, **kwargs):
        return {"p": self.p , "tau" : self.tau}


    def suggest_param_range(self,X):
        return {"p" : [1,2,3] , "tau": [0.0005,0.001,0.002,0.004,0.008,0.01,0.02,0.04,0.08]}


    def fit(self, X, y=None): ## no fitting
        self.is_fitted = True
        return self

    def repair(self,injected,truth, columns_to_repair , labels=None):
        assert truth is not None , "IMR needs truth values to assign labels"
        assert labels is not None  ,  "IMR requires labels"

        injected = injected.copy()
        truth_full = truth.copy()
        repair = injected.copy()
        for col in columns_to_repair:
            x = np.array(injected)[:, col]
            truth = np.array(truth_full)[:, col]
            if np.allclose(x,truth):
                assert False ,(x,truth)
                repair.iloc[:, col] = x

            col_labels = labels.iloc[:,col]

            col_labels = np.arange(len(col_labels))[col_labels]

            y_0 = x.copy()
            y_0[col_labels] = truth[col_labels]

            if  np.allclose(x, y_0):
                pass

            repair_results = imr(x, y_0, col_labels, tau=self.tau, p=self.p, k=self.max_itr_n)
            col_repair = repair_results["repair"]
            repair.iloc[:, col] = col_repair

        return repair

    @property
    def alg_type(self):
        return IMR

    def __str__(self):
        return  f'IMR({self.p},{round(self.tau,2)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()