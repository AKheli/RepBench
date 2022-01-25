from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
from sklearn.metrics import  f1_score

from Repair.Robust_PCA.robust_PCA_estimator import Robust_PCA_estimator


class Robust_PCA_classifier(Robust_PCA_estimator):
    def predict(self, X):
        X = X.copy()
        X = self._validate_data(X, dtype=[np.float32], reset=False)
        X_reduced = self.reduce(X)
        anoms = pd.DataFrame(self.classify_anomalies(X, X_reduced))
        return anoms

    def score(self, X, y,predict= False):
        predicted_anoms = self.predict(X)
        print("sum",np.sum(np.array(predicted_anoms)))
        print("sum non", np.sum(np.invert(np.array(predicted_anoms))))
        t = []
        p = []
        for col in self.cols:
            injected_col = np.array(X)[:,col]

            truth_col =  np.array(y)[:,col]
            predicted_col = predicted_anoms[col]
            true_anomalies = injected_col != truth_col
            t.append(true_anomalies)
            p.append(predicted_col)

        t  = np.concatenate(t, axis=None,dtype=int)
        p  = np.concatenate(p, axis=None,dtype=int)

        #print(f1_score(np.concatenate(t, axis=None),np.concatenate(p, axis=None)))
        print(np.sum(np.abs(t-p)))
        np.sum( (t - p) >0)**1.5 + np.sum( (t - p) < 0 )
        return -(np.sum( (t - p) >0)**2 + np.sum( (t - p) < 0 ))/len(p)
