from Repair.Dimensionality_Reduction.difference_classifier import difference_classify
from Repair.cdrec.recovery import centroid_decomposition, centroid_recovery

import numpy as np


class CD_Rec_estimator():
    def __init__(self
                 , truncation=2
                 , threshold=0.1
                 , center=True
                 , **kwargs
                 ):
        self.truncation = truncation
        self.threshold = threshold
        self.center = center

    def reduce(self, matrix):
        if self.center:
            col_mean = matrix.mean(axis=0)
            matrix = matrix - col_mean

        L, R, Z = centroid_decomposition(matrix * 1, truncation=self.truncation)
        self.L = L
        self.R = R
        self.Z = Z

        if self.center:
            reduced = np.matmul(L, R.T) + col_mean
        else:
            reduced = np.matmul(L, R.T)

        return reduced

    def classify(self, matrix):
        reduced = self.reduce(matrix)
        diff = matrix - reduced
        anomaly_matrix = difference_classify(diff, self.threshold)
        return anomaly_matrix

    def repair(self, matrix, anomaly_matrix=None):
        if anomaly_matrix is None:
            anomaly_matrix = self.classify(matrix)

        assert matrix.shape == anomaly_matrix.shape

        anomaly_cleared_matrix = matrix.copy()
        anomaly_cleared_matrix[anomaly_matrix] = np.nan
        repair = centroid_recovery(anomaly_cleared_matrix, truncation=self.truncation)

        return repair
