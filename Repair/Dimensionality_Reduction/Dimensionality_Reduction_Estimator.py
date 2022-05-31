import numpy as np
import pandas as pd
from Repair.Dimensionality_Reduction.interpolation import interpolate
from Repair.estimator import Estimator
from sklearn.utils import check_array


class DimensionalityReductionEstimator(Estimator):
    def __init__(self, classification_truncation=1
                 , repair_truncation=2
                 , delta=1.5
                 , threshold=0.3
                 , eps=1e-6
                 , n_max_iter=15
                 , repair_iter = 2
                 , interpolate_anomalies=True
                 , sub_set = False
                 , **kwargs
                 ):
        self.threshold = threshold
        self.interpolate_anomalies = interpolate_anomalies
        self.delta = delta
        self.classification_truncation = classification_truncation
        self.repair_truncation = repair_truncation
        self.eps = eps
        self.n_max_iter = n_max_iter
        self.repair_iter = repair_iter
        self.sub_set = sub_set
        super().__init__(**kwargs)

    def get_fitted_params(self, deep=False):
        return {"classification_truncation": self.classification_truncation,
                "repair_truncation": self.repair_truncation,
                "threshold": self.threshold,
                "repair_iter": self.repair_iter,
                "n_max_iter": self.n_max_iter,
                "sub_set": self.sub_set}

    def suggest_param_range(self, X):
        n_cols = X.shape[1]
        return {"classification_truncation": [i for i in [1,2,3,4,5,6,7,8] if i < n_cols-1],
                "repair_truncation": [i for i in [2,3,4,5,6,7,8] if i < n_cols-1],
                "threshold": [0.1,1.5,2,2.5,3,5],
                "repair_iter" : [0,5],
                "n_max_iter": [0,20]
                }

    def fit(self, X, y=None):
        self.reduce(X, self.classification_truncation)
        self.is_fitted = True
        assert hasattr(self, "transform_matrix")
        return self

    def reduce(self, matrix, truncation):
        matrix = matrix.copy()
        n,m = matrix.shape
        if truncation >= m:
            truncation = m-1

        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        transform_matrix, weighted_mean, weights = self.IRLS(matrix, truncation)
        assert np.linalg.matrix_rank(transform_matrix) == truncation
        self.transform_matrix = transform_matrix
        self.weighted_mean = weighted_mean

        reduced = self.transform_(matrix)

        return reduced


    def transform_(self, matrix):
        return np.dot(matrix - self.weighted_mean, self.transform_matrix) + self.weighted_mean

        # def fitted_transform_(self,matrix):


    def predict(self, matrix, y=None  , refit = True , labels=None):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        matrix_to_repair = matrix.copy()

        if (self.sub_set):
            if len(self.columns_to_repair) == 1:
                sorted_corr = np.argsort(-np.abs(np.corrcoef(matrix,rowvar=False)[self.columns_to_repair,:]))[0]
                matrix_to_repair[:,sorted_corr[6:]] = 0
                assert np.any(matrix_to_repair[:,self.columns_to_repair])

        reduced = self.reduce(matrix_to_repair, self.classification_truncation)

        anomaly_matrix = self.classify(matrix_to_repair, reduced=reduced)

        assert matrix_to_repair.shape == anomaly_matrix.shape

        matrix_to_interpolate = matrix_to_repair.copy()
        matrix_to_interpolate[anomaly_matrix] = np.nan
        matrix_inter = interpolate(matrix_to_interpolate, anomaly_matrix)
        assert not np.isnan(matrix_inter).any(), "interpolation failed"

        reduced = matrix_inter
        for i in range(self.repair_iter):
            reduced = self.reduce(reduced, self.repair_truncation)
            matrix_to_repair[anomaly_matrix] = reduced[anomaly_matrix]
            reduced = matrix_to_repair.copy()


        final = matrix.copy()
        final[:,self.columns_to_repair] = matrix_to_repair[:,self.columns_to_repair]
        return pd.DataFrame(final)


    def IRLS(self, matrix, truncation):
        X = check_array(matrix, dtype=[np.float32], ensure_2d=True,
                        copy=True)
        n_samples, n_features = X.shape
        weights = np.ones(n_samples)
        n_iterations_ = 1
        last_error = np.inf

        not_done_yet = True
        while not_done_yet:
            weighted_mean = np.average(X, axis=0, weights=weights)
            X_centered = X - weighted_mean
            transform_matrix = self.compute_transform(X_centered * np.sqrt(weights.reshape(-1, 1)), truncation)
            assert transform_matrix.shape == (n_features, n_features), transform_matrix.shape
            diff = X_centered - np.dot(X_centered, transform_matrix)
            errors_raw = np.linalg.norm(diff, axis=1)
            self.errors_raw = errors_raw
            errors_loss = compute_loss(errors_raw, self.delta)
            total_error = errors_loss.sum()

            weights = compute_weights(errors_raw, self.delta)

            n_iterations_ += 1

            not_done_yet = n_iterations_ < self.n_max_iter
                          # or abs(total_error - last_error) / abs(total_error) < 0.00000000000001

        return transform_matrix, weighted_mean, weights


    def classify(self, matrix, reduced):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values
        assert matrix.shape == reduced.shape
        diff = matrix - reduced
        anomaly_matrix = difference_classify(diff, self.columns_to_repair, self.threshold)
        return anomaly_matrix




def z_score(x, threshold):
    x_abs = np.abs(x)

    x_normalized = (x_abs - np.mean(x_abs)) / np.std(x_abs)
    return x_normalized > threshold


def difference_classify(diff_matrix, injected_columns, threshold):
    m = diff_matrix.shape[1]
    anomaly_matrix = np.zeros_like(diff_matrix, dtype=bool)
    for i in [k for k in range(m) if k in injected_columns]:
        anomaly_matrix[:, i] = z_score(diff_matrix[:, i], threshold)
        anomaly_matrix[:3, i], anomaly_matrix[-3:, i] = False, False
    return anomaly_matrix


def compute_loss(x, delta):
    delta_half_square = (delta ** 2) / 2.
    smaller = x <= delta
    bigger = np.invert(smaller)
    result = np.zeros_like(x)
    result[smaller] = x[smaller] ** 2 / 2.
    result[bigger] = delta * x[bigger] - delta_half_square
    return result


def compute_weights(x, delta):
    return 1.0 * (x < delta) + ((x >= delta) / x)
