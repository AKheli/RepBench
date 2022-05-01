import pandas as pd
from matplotlib import pyplot as plt

from Repair.algorithms_config import IMR
from Repair.IMR.IMR import imr2
from Repair.IMR.label_generator import generate_anomaly_start_labels, generate_random_labels
from Repair.estimator import Estimator
import numpy as np


alg_type = IMR
class IMR_estimator(Estimator):

    def __init__(self, p=5,tau = 0.1, **kwargs):
        self.p = p
        self.tau = tau
        self.alg_type = alg_type
        Estimator.__init__(self, **kwargs)
        self.max_itr_n  = 1000

    def get_params(self, **kwargs):
        return {"p": self.p , "tau" : self.tau , "columns_to_repair" : self.columns_to_repair}


    def suggest_param_range(self,X):
        return {"p" : list(range(15))} # , "tau": list(np.arange(100)/100) }


    def fit(self, X, y=None): ## no fitting
        self.is_fitted = True
        return self

    def predict(self, X , y =None):
        # print(self.cols)
        # X.iloc[:,self.cols].plot()
        # plt.show()
        # y.iloc[:,self.cols].plot()
        # plt.show()
        assert y is not None , "IMR needs truth values to assign labels"

        injected = X.copy()
        truth = y.copy()
        repair = injected.copy()
        for col in self.columns_to_repair:
            x = np.array(injected.iloc[:, col])
            truth = np.array(truth.iloc[:, col])
            if np.allclose(x,truth):
              assert False, "x and y_0 initialization are to close for a repair"
              repair.iloc[:, col] = x

            anom_start_labels = generate_anomaly_start_labels(x, truth,
                                                              start_of_anomaly=True)

            labels = generate_random_labels(x, label_ratio=0.2, first_labels=self.p + 3,
                                                already_labeled=anom_start_labels)

            labels = np.arange(len(labels))[labels]

            y_0 = x.copy()
            y_0[labels] = truth[labels]
            # plt.plot(labels, y_0[labels], ls="", marker="x",color = "blue")
            # plt.plot(X.iloc[:, self.cols],ls="",marker=".",ms=2,color="red")
            #plt.plot(y_0)

            # plt.show()
            #
            # plt.plot(X.iloc[:, col].values-y_0)
            # #y.iloc[:, self.cols].plot()
            # plt.show()
            if  np.allclose(x, y_0):
                pass
                # plt.plot(x)
                # plt.plot(truth)
                # plt.show()
                # plt.plot(y_0)
                # plt.show()

            # print("eeeeeeeeeee" ,self.tau)
            # print(self.p)
            # print(self.max_itr_n)
            repair_results = imr2(x, y_0, labels, tau=self.tau, p=self.p, k=self.max_itr_n)
            col_repair = repair_results["repair"]

            # print(sum(col_repair-x)-sum((col_repair-x)[labels]))
            # print(sum(x-truth))
            # plt.plot(col_repair)
            # plt.show()
            # plt.plot(x)
            # plt.show()
            # plt.plot(y_0)
            # plt.show()
            # plt.plot(labels)
            # plt.show()
            # print(labels)
            repair.iloc[:, col] = col_repair


        return repair

    def alg_type(self):
        return "IMR"

    def __str__(self):
        return  f'IMR({self.p},{round(self.tau,2)})'

    def get_fitted_attributes(self):
        return self.get_params()