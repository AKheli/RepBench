from matplotlib import pyplot as plt

from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
import pandas as pd
import numpy as np
from sklearn.metrics import  f1_score

class Robust_PCA_classifier(Robust_PCA_estimator):
    def predict(self, X):
        X = X.copy()
        X = self._validate_data(X, dtype=[np.float32], reset=False)
        X_reduced = self.reduce(X)
        anoms = pd.DataFrame(self.classifiy_anomalies(X, X_reduced))
        return anoms

    def score(self, X, y):
        predicted_anoms = self.predict(X)

        t = []
        p = []
        for col in self.cols:
            injected_col = np.array(X)[:,col]

            truth_col =  np.array(y)[:,col]
            predicted_col = predicted_anoms[col]
            true_anomalies = injected_col != truth_col
            t.append(true_anomalies)
            p.append(predicted_col)

        t  = np.concatenate(t, axis=None)
        p  = np.concatenate(p, axis=None)

        print(f1_score(np.concatenate(t, axis=None),np.concatenate(p, axis=None)))
        return f1_score(np.concatenate(t, axis=None),np.concatenate(p, axis=None))