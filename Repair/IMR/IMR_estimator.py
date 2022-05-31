import pandas as pd
from Repair.algorithms_config import IMR
from Repair.IMR.IMR import imr2
from Repair.estimator import Estimator
import numpy as np
import run_ressources.Logger as log

class IMR_estimator(Estimator):

    def __init__(self, p=5,tau = 0.1, **kwargs):
        self.p = p
        self.tau = tau
        Estimator.__init__(self, **kwargs)
        self.max_itr_n  = 100

    def get_fitted_params(self, **kwargs):
        return {"p": self.p , "tau" : self.tau}


    def suggest_param_range(self,X):
        return {"p" : [1,2,3,5,16] , "tau": [0.0005,0.001,0.002,0.004,0.008,0.01,0.02,0.04,0.08,0.1,0.2,0.5]}


    def fit(self, X, y=None): ## no fitting
        self.is_fitted = True
        return self

    def predict(self, X , y = None , labels = None):
        assert y is not None , "IMR needs truth values to assign labels"
        assert labels is not None  ,  "IMR requires labels"

        injected = X.copy()
        truth_full = y.copy()
        repair = injected.copy()
        for col in self.columns_to_repair:
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

            repair_results = imr2(x, y_0, col_labels, tau=self.tau, p=self.p, k=self.max_itr_n)
            col_repair = repair_results["repair"]
            repair.iloc[:, col] = col_repair

            min_label = min(labels)

        return repair

    @property
    def alg_type(self):
        return IMR

    def __str__(self):
        return  f'IMR({self.p},{round(self.tau,2)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()