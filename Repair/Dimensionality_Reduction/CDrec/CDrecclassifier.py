from Repair.Dimensionality_Reduction.RobustPCA.vadetis.loss import HuberLoss
from Repair.Dimensionality_Reduction.difference_classifier import difference_classify
from Repair.cdrec.recovery import centroid_decomposition, centroid_recovery

import numpy as np


class CD_Rec_estimator():
    def __init__(self
                 , truncation=2
                 , threshold=0.1
                 , delta = 0.01
                 , **kwargs
                 ):
        self.loss = HuberLoss(delta)
        self.truncation = truncation
        self.threshold = threshold
        self.eps =1e-8
        self.max_iter= 100

    def reduce(self, matrix):
        X = matrix.copy()
        vectorized_loss = np.vectorize(self.loss.__call__)
        vectorized_weights = np.vectorize(self.loss.weight)

        n_samples, n_features = X.shape

        self.weights_ = 1. / n_samples * np.ones(n_samples)
        self.errors_ = [np.inf]
        self.n_iterations_ = 0
        not_done_yet = True
        while not_done_yet:
            self.mean_ = np.average(X, axis=0, weights=self.weights_)
            X_centered = X - self.mean_

            L, R, Z = centroid_decomposition(X_centered * 1, truncation=self.truncation)
            self.L = L
            self.R = R
            self.Z = Z
            reduced = np.matmul(L, R.T)
            diff=  X_centered - reduced
            errors_raw =  np.linalg.norm(diff, axis=1)
            errors_loss = vectorized_loss(errors_raw)

            self.weights_ = vectorized_weights(errors_raw)
            self.weights_ /= self.weights_.sum()

            # Checking stopping criteria
            self.n_iterations_ += 1
            old_total_error = self.errors_[-1]
            total_error = errors_loss.sum()
            print(total_error)
            if not np.equal(total_error, 0.):
                rel_error = abs(total_error - old_total_error) / abs(total_error)
            else:
                rel_error = 0.

            self.errors_.append(total_error)
            not_done_yet = self.n_iterations_ < self.max_iter and rel_error > self.eps

        return np.matmul(L, R.T) + self.mean_

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
