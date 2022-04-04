import numpy as np

from Repair.Dimensionality_Reduction.difference_classifier import difference_classify
from Repair.Dimensionality_Reduction.interpolation import interpolate
from Repair.estimator import estimator


class DimensionalityReductionEstimator(estimator):
    def __init__(self, classification_truncation=1
                 , repair_truncation = 1
                 , delta=0.001
                 , threshold=0.4
                 , eps=1e-6
                 , max_iter=100
                 , interpolate_anomalies=True
                 , **kwargs
                 ):
        self.threshold = threshold
        self.interpolate_anomalies = interpolate_anomalies
        self.delta = delta
        self.classification_truncation = classification_truncation
        self.classificatrepair_truncation = repair_truncation
        self.eps = eps
        self.max_iter = max_iter
        super().__init__(**kwargs)

    def suggest_param_range(self, X):
        # todo smin and smax suggestion
        return {"truncation": list(range(1, X.shape[1])),
                "delta": np.logspace(0, 1, num=100),
                "threshold": np.linspace(0, 1, num=50)}

    def _fit(self, X, y=None):
        self.reduce(X)
        self.is_fitted = True
        return self

    def _predict(self, matrix, y=None):
        if y is not None:
            anomaly_matrix = matrix != y
        else:
            anomaly_matrix = None

        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        reduced = self.reduce(matrix)

        if anomaly_matrix is None:
            anomaly_matrix = self.classify(matrix, reduced=reduced)

        assert matrix.shape == anomaly_matrix.shape

        repair = matrix.copy()

        if self.interpolate_anomalies:
            matrix_to_interpolate = matrix.copy()
            matrix_to_interpolate[anomaly_matrix] = np.nan
            matrix_inter = interpolate(matrix_to_interpolate, anomaly_matrix)
            reduced = self.reduce(matrix_inter)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        else:
            reduced = self.reduce(matrix)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        return repair

    def classify(self, matrix, reduced=None):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        if reduced is None:
            reduced = self.reduce(matrix)
        assert matrix.shape == reduced.shape
        diff = matrix - reduced
        anomaly_matrix = difference_classify(diff, self.threshold, self.cols)
        return anomaly_matrix
