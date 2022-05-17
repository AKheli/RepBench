import pandas as pd
from matplotlib import pyplot as plt

from Repair.algorithms_config import IMR
from Repair.IMR.IMR import imr2
from Repair.IMR.label_generator import generate_anomaly_start_labels, generate_random_labels
from Repair.estimator import Estimator
import numpy as np
import run_ressources.Logger as log

alg_type = IMR
class IMR_estimator(Estimator):

    def __init__(self, p=5,tau = 0.1, **kwargs):
        self.p = p
        self.tau = tau
        self.alg_type = alg_type
        Estimator.__init__(self, **kwargs)
        self.max_itr_n  = 100

    def get_fitted_params(self, **kwargs):
        return {"p": self.p , "tau" : self.tau}


    def suggest_param_range(self,X):
        return {"p" : list(range(15)) , "tau": [0.01,0.005,0.001,0.0005]}


    def fit(self, X, y=None): ## no fitting
        self.is_fitted = True
        return self

    def predict(self, X , y =None , labels = None):
        assert y is not None , "IMR needs truth values to assign labels"
        assert labels is not None  or self.train_call_back is not None, "IMR requires labels"


        #in case of cv when labels are not aviable assign random labels
        if labels is None and self.train_call_back.labels.shape != X.shape:
            np.random.seed(100)
            labels = pd.DataFrame(np.random.binomial(1,0.5,X.shape))


        injected = X.copy()
        truth_full = y.copy()
        repair = injected.copy()
        for col in self.columns_to_repair:
            x = np.array(injected)[:, col]
            truth = np.array(truth_full)[:, col]
            if np.allclose(x,truth):
                log.add_to_log("x and y_0 initialization are to close for a repair")
                if not log.do_log:
                    assert False ,"x and y_0 initialization are to close for a repair"
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


        return repair

    def alg_type(self):
        return "IMR"

    def __str__(self):
        return  f'IMR({self.p},{round(self.tau,2)})'

    def get_fitted_attributes(self):
        return self.get_fitted_params()