from Repair.Dimensionality_Reduction.CDrec.recovery import interpolate
from Repair.Dimensionality_Reduction.RobustPCA.reduction import fit_components
from Repair.Dimensionality_Reduction.difference_classifier import difference_classify
from Repair.estimator import estimator
import numpy as np

class Robust_PCA_estimator(estimator):

    def __init__(self, n_components=2
                 , cols=[0]
                 , delta=0.1
                 , threshold=0.1
                 , eps=1e-8
                 , max_iter=50
                 , interpolate_anomalies=True
                 , center=True
                 , **kwargs
                 ):
        self.threshold = threshold
        self.interpolate_anomalies = interpolate_anomalies
        self.cols = cols
        self.delta = delta
        self.n_components = n_components
        self.eps = eps
        self.max_iter = max_iter
        self.center = center
        super().__init__(**kwargs)

    def reduce(self, matrix):
        if self.center:
            col_mean = matrix.mean(axis=0)
            matrix = matrix - col_mean

        C = fit_components(matrix, self.n_components, self.delta , max_iter  = self.max_iter)

        if self.center:
            reduced = np.dot(matrix, C.T).dot(C) + col_mean
        else:
            reduced =  np.dot(matrix, C.T).dot(C)

        return reduced

    def classify(self, matrix , reduced = None):
        if reduced is None:
            reduced = self.reduce(matrix)
        assert matrix.shape == reduced.shape
        diff = matrix - reduced
        anomaly_matrix = difference_classify(diff, self.threshold)
        return anomaly_matrix

    ## add fit() for train and check if it is fitted on predict and reduce

    def repair(self, matrix, anomaly_matrix=None):
        reduced = self.reduce(matrix)
        if anomaly_matrix is None:
            anomaly_matrix = self.classify(matrix,reduced=reduced)

        assert matrix.shape == anomaly_matrix.shape

        repair = matrix.copy()

        if self.interpolate_anomalies:
            matrix_to_interpolate = matrix.copy()
            matrix_to_interpolate[anomaly_matrix] = np.nan
            matrix = interpolate(matrix_to_interpolate,anomaly_matrix)
            reduced = self.reduce(matrix)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        else:
            reduced = self.reduce(matrix)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        return repair
