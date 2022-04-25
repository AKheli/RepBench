import numpy as np
import pandas as pd
from Repair.Dimensionality_Reduction.interpolation import interpolate
from Repair.estimator import estimator
from scipy import linalg
from sklearn.decomposition import TruncatedSVD
from sklearn.utils import check_array

class DimensionalityReductionEstimator(estimator):
    def __init__(self, classification_truncation=1
                 , repair_truncation = 2
                 , delta=1.5
                 , threshold=0.3
                 , eps=1e-6
                 , max_iter=10
                 , interpolate_anomalies=True
                 , **kwargs
                 ):
        self.threshold = threshold
        self.interpolate_anomalies = interpolate_anomalies
        self.delta = delta
        self.classification_truncation = classification_truncation
        self.repair_truncation = repair_truncation
        self.eps = eps
        self.n_max_iter = max_iter

        super().__init__(**kwargs)


    def normalize(self,X):
        self.norm_std = np.std(X,axis=0)
        self.norm_mean = np.mean(X,axis=0)
        return (X-self.norm_mean)/self.norm_std

    def undo_normalization(self,X):
        X = X*self.norm_std+self.norm_mean
        self.norm_std = None
        self.norm_mean = None
        return X

    def get_params(self,deep = False):
        return self.__dict__

    def get_fitted_attributes(self):
        return {"classification_truncation": self.classification_truncation,
                "repair_truncation": self.repair_truncation,
                #"delta": self.delta,
                "threshold": self.threshold}

    def suggest_param_range(self, X):
        n_cols = X.shape[1]
        return {"classification_truncation": list(range(1, max(2,min(int(X.shape[1]/2),3)))),
                "repair_truncation": list(range(1, max(2,min(4,n_cols-1)))),
                #"delta": np.geomspace(0.001, np.mean(np.linalg.norm(X,axis=1))/3, num=30),
                "threshold": np.linspace(1, 2.8, num=20)}

    def _fit(self, X, y=None):
        self.reduce(X,self.classification_truncation)
        self.is_fitted = True
        return self


    def _reduce(self, matrix, truncation):
        matrix = matrix.copy()
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        transform_matrix, weighted_mean, weights = self.IRLS(matrix,truncation)
        reduced = np.dot(matrix - weighted_mean, transform_matrix) + weighted_mean

        return reduced


    def _predict(self, matrix, y=None):

        anomaly_matrix = None

        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values



        if anomaly_matrix is None:
            reduced = self.reduce(matrix, self.classification_truncation)
            anomaly_matrix = self.classify(matrix, reduced=reduced)

        assert matrix.shape == anomaly_matrix.shape

        repair = matrix.copy()

        if self.interpolate_anomalies:
            matrix_to_interpolate = matrix.copy()
            matrix_to_interpolate[anomaly_matrix] = np.nan
            matrix_inter = interpolate(matrix_to_interpolate, anomaly_matrix)

            assert not np.isnan(matrix_inter).any() , matrix_inter

            reduced = self.reduce(matrix_inter,self.repair_truncation)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        else:
            reduced = self.reduce(matrix)
            repair[anomaly_matrix] = reduced[anomaly_matrix]

        return repair

    def classify(self, matrix, reduced=None):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        if reduced is None:
            reduced = self.reduce(matrix,self.classification_truncation)
        assert matrix.shape == reduced.shape
        diff = matrix - reduced
        anomaly_matrix = self.difference_classify(diff, self.cols)
        return anomaly_matrix

    def reduce(self,matrix,truncation):
        matrix = np.asarray(matrix, dtype=np.float64).copy()
        norm_matrix = self.normalize(matrix)
        matrix_hat = self._reduce(norm_matrix,truncation)
        return self.undo_normalization(matrix_hat)


    ## classification_methods
    def min_max(self,x):
        x_abs = abs(x)  #todo check whitout training and abs or not
        if(self.is_training):
            self.train_min = min_ = min(x_abs)
            self.train_max = max_ =  max(x_abs)
        elif hasattr(self,"train_min") and hasattr(self,"train_max"):
            min_ = self.train_min
            max_ = self.train_max
        else:
            min_ = min(x)
            max_ = max(x)

        x_normalized = (x_abs - min_) / (max_ - min_)
        return x_normalized > self.threshold

    def z_score(self,x):
        x_abs = np.abs(x)

        x_normalized = (x_abs - np.mean(x_abs))/np.std(x_abs)
        return x_normalized > self.threshold

    def difference_classify(self, diff_matrix, injected_columns):
        m = diff_matrix.shape[1]
        anomaly_matrix = np.zeros_like(diff_matrix, dtype=bool)
        for i in [k for k in range(m) if k in injected_columns]:
            anomaly_matrix[:, i] = self.z_score(diff_matrix[:, i])
            anomaly_matrix[:3, i] , anomaly_matrix[-3:, i] = False , False
        return anomaly_matrix


    def IRLS(self,matrix,truncation):
        X = check_array(matrix, dtype=[np.float32], ensure_2d=True,
                        copy=True)
        n_samples, n_features = X.shape
        weights =  np.ones(n_samples)
        n_iterations_ = 1
        not_done_yet = True
        last_error = np.inf

        while not_done_yet:
            weighted_mean = np.average(X, axis=0, weights=weights)
            X_centered = X - weighted_mean
            transform_matrix = self.compute_transform(X_centered * np.sqrt(weights.reshape(-1, 1)), truncation)
            assert transform_matrix.shape == (n_features,n_features) ,transform_matrix.shape
            diff = X_centered - np.dot(X_centered, transform_matrix)
            errors_raw = np.linalg.norm(diff, axis=1)

            errors_loss = compute_loss(errors_raw, self.delta)
            total_error = errors_loss.sum()

            weights = compute_weights(errors_raw, self.delta)

            n_iterations_ += 1

            not_done_yet = n_iterations_ < self.n_max_iter \
                           or abs(total_error - last_error) / abs(total_error) < 0.00000000000001

        return transform_matrix, weighted_mean, weights



def compute_loss(x,delta):
    delta_half_square = (delta ** 2) / 2.
    smaller = x <= delta
    bigger = np.invert(smaller)
    result = np.zeros_like(x)
    result[smaller] = x[smaller] ** 2 / 2.
    result[bigger] = delta * x[bigger] - delta_half_square
    return result


def compute_weights(x,delta):
    return 1.0*(x<delta)+((x>=delta)/x)