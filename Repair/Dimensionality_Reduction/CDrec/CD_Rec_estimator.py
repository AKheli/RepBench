import pandas as pd
from matplotlib import pyplot as plt

from Repair.Algorithms_Config import CDREC
from Repair.Dimensionality_Reduction.CDrec.weighted_cedomposition import weighted_centroid_decomposition
from Repair.Dimensionality_Reduction.Dimensionality_Reduction_Estimator import DimensionalityReductionEstimator
from Repair.Robust_PCA.loss import HuberLoss
import numpy as np


class CD_Rec_estimator(DimensionalityReductionEstimator):

    def _reduce(self, matrix, truncation):
        assert matrix[:, 0].std() < 1.01 and matrix[:, 0].mean() < 0.01 and matrix[:, 0].mean() > -0.01

        self.loss = HuberLoss(self.delta)
        X = matrix.copy()
        vectorized_loss = np.vectorize(self.loss.__call__)
        vectorized_weights = np.vectorize(self.loss.weight)


        self.mean_ = np.average(X, axis=0)
        X_centered = X - self.mean_

        L, R, Z = weighted_centroid_decomposition(X_centered * 1, truncation=truncation, weights=None)
        self.L = L
        self.R = R
        self.Z = Z
        reduced = np.matmul(L, R.T)
        assert reduced.shape == X.shape
        diff = X_centered - reduced
        errors_raw = np.linalg.norm(diff, axis=1)
        self.weights_ = vectorized_weights(errors_raw)

        self.weights = self.weights_
        return np.matmul(L, R.T) + self.mean_


    @property
    def alg_type(self):
        return CDREC

    def algo_name(self):
        return f'CDrec({self.classification_truncation},{self.repair_truncation},{self.delta},{round(self.threshold,2)})'
