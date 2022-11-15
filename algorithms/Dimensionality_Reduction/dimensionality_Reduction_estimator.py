import numpy as np
import pandas as pd
from algorithms.Dimensionality_Reduction.interpolation import interpolate
from algorithms.estimator import Estimator
from sklearn.utils import check_array

from data_methods.data_class import normalize_f


class DimensionalityReductionEstimator(Estimator):
    def __init__(self, classification_truncation=2
                 , repair_truncation=4
                 , delta=1.5
                 , threshold=1.2
                 , eps=1e-6
                 , n_max_iter=50
                 , repair_iter=10
                 , windows=False
                 , **kwargs
                 ):
        self.threshold = threshold
        self.delta = delta
        self.classification_truncation = classification_truncation
        self.repair_truncation = repair_truncation
        self.eps = eps
        self.n_max_iter = n_max_iter
        self.repair_iter = repair_iter
        self.reduced_ = None
        self.windows = windows
        self.additional_plotting_args = {}
        self.state = None
        self.normalize_before = True

        self.weights_i_ = {}
        self.reduced_i_ = {}

    def get_fitted_params(self, deep=False):
        return {"classification_truncation": self.classification_truncation,
                "repair_truncation": self.repair_truncation,
                "threshold": self.threshold,
                "repair_iter": self.repair_iter,
                "n_max_iter": self.n_max_iter,
                }

    ##todo add dtype
    def suggest_param_range(self, X=None):
        n_cols = X.shape[1] if X is not None else 10
        return {"classification_truncation": [i for i in [1, 2, 3, 4, 5] if i < n_cols - 1],
                "repair_truncation": [i for i in [2, 3, 4, 5] if i < n_cols - 1],
                "threshold": [1.0, 1.2, 1.5, 2.0, 2.5, 3.0],
                "repair_iter": [1, 10],
                "n_max_iter": [1, 20],  # reweighting
                }

    def reduce(self, matrix, truncation):
        matrix = matrix.copy()
        n, m = matrix.shape
        if truncation >= m:
            truncation = m - 1

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

    def repair(self, injected, truth, columns_to_repair, labels=None):
        truth = None
        self.weights_i_ = {}
        if self.normalize_before:
            injected, inv_f = normalize_f(injected)

        self.state = "classify"
        self.weights_i_[self.state] = {}
        self.reduced_i_[self.state] = {}

        self.columns_to_repair = columns_to_repair
        if isinstance(injected, pd.DataFrame):
            matrix = injected.values

        matrix_to_repair = matrix.copy()

        reduced = self.reduce(matrix_to_repair, self.classification_truncation)
        self.reduced = reduced

        ## classify anomalies
        self.anomaly_matrix = classify(matrix_to_repair, reduced=reduced , columns_to_repair = columns_to_repair , threshold=self.threshold)

        assert matrix_to_repair.shape == self.anomaly_matrix.shape
        self.state = "repair"
        self.weights_i_[self.state] = {}
        self.reduced_i_[self.state] = {}
        matrix_to_interpolate = matrix_to_repair.copy()
        matrix_to_interpolate[self.anomaly_matrix] = np.nan
        matrix_inter = interpolate(matrix_to_interpolate, self.anomaly_matrix)
        assert not np.isnan(matrix_inter).any(), "interpolation failed"

        reduced = matrix_inter
        for i in range(self.repair_iter):
            reduced = self.reduce(reduced, self.repair_truncation)
            matrix_to_repair[self.anomaly_matrix] = reduced[self.anomaly_matrix]
            reduced = matrix_to_repair.copy()
        self.reduced_ = reduced

        final = matrix.copy()
        final[:, columns_to_repair] = matrix_to_repair[:, columns_to_repair]

        result = injected.copy()
        result.loc[:] = final
        assert injected.shape == result.shape
        if self.normalize_before:
            result = inv_f(result)
        return result

    def IRLS(self, matrix, truncation):
        X = check_array(matrix, dtype=[np.float32], ensure_2d=True,
                        copy=True)
        n_samples, n_features = X.shape
        weights = np.ones(n_samples) / n_samples
        last_error = np.inf

        for n_iter in range(self.n_max_iter):
            weighted_mean = np.average(X, axis=0, weights=weights)
            X_centered = X - weighted_mean
            transform_matrix = self.compute_transform(X_centered * np.sqrt(weights.reshape(-1, 1)), truncation)
            assert transform_matrix.shape == (n_features, n_features), transform_matrix.shape
            reduced_centered = np.dot(X_centered, transform_matrix)
            diff = X_centered - reduced_centered
            self.weights_i_[self.state][n_iter] = weights
            self.reduced_i_[self.state][n_iter] = reduced_centered + weighted_mean
            errors_raw = np.linalg.norm(diff, axis=1)
            self.errors_raw = errors_raw
            errors_loss = compute_loss(errors_raw, self.delta)
            weights = compute_weights(errors_raw, self.delta)
            self.weights = weights

            # or abs(total_error - last_error) / abs(total_error) < 0.00000000000001
        return transform_matrix, weighted_mean, weights


def classify(matrix, reduced, columns_to_repair, threshold):
    if isinstance(matrix, pd.DataFrame):
        matrix = matrix.values
    assert matrix.shape == reduced.shape
    diff = matrix - reduced
    anomaly_matrix = difference_classify(diff, columns_to_repair, threshold)
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
    assert not any(x < 0)
    return 1.0 * (x < delta) + ((x >= delta) * delta / x)
