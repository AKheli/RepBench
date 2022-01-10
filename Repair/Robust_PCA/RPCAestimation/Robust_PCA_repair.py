import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import linalg
from scipy.sparse import issparse
from sklearn.base import BaseEstimator
from sklearn.utils import check_array
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import FastICA

from Repair.Algorithms_File import RPCA, ALGORITHM_PARAMETERS
from Repair.res.timer import Timer
import warnings

# transforming
from Scenarios.metrics import RMSE

warnings.simplefilter("ignore", UserWarning)  # feaure name

alg_type = RPCA
default_params = ALGORITHM_PARAMETERS[alg_type]


def RPCA_repair(injected, cols, n_components=1, threshold=2.2, window = False, **args):
    if window:
        return RPCA_repair_window(injected, cols, n_components=n_components, threshold=threshold, **args)
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    timer = Timer()
    timer.start()
    np.random.seed(100)
    PCA_method = args.get("PCA_method","TruncatedSVD")
    pca = Robust_PCA_estimator(cols=cols, n_components=n_components, threshold=threshold , component_method= PCA_method)
    sampled = injected.sample(n=1000, axis='rows', replace=True)
    pca.fit(sampled)
    repair = pd.DataFrame(pca.predict(injected))
    repair.columns = list(injected.columns)

    return {"repair": repair, "runtime": timer.get_time(), "n_components": n_components
        , "threshold": threshold, "type": alg_type  , "name" : f'RPCA({n_components},{round(threshold,2)},{PCA_method})'}



def RPCA_repair_window(injected, cols, n_components=1, threshold=2.2, **args):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass
    repair = injected.copy()

    window_size = 2000
    total_size = len(injected)

    timer = Timer()
    timer.start()
    PCA_method = args.get("PCA_method","TruncatedSVD")
    pca = Robust_PCA_estimator(cols=cols, n_components=n_components, threshold=threshold , component_method= PCA_method)

    for i in range(max(1,int(total_size/window_size))):
        # repair.plot()
        # plt.show()
        if i == int(total_size/window_size):
            X_window = repair.iloc[i*window_size:,:]
            pca.fit(X_window)
            plt.gca().set_prop_cycle(None)
            comp = list(pca.components_[0,:])
            for c in comp:
                plt.plot(i,c,marker="x")
            repair.iloc[i * window_size:, :] = pd.DataFrame(pca.predict(X_window))
        else:
            X_window = repair.iloc[i * window_size:(i+1)*window_size, :]
            pca.fit(X_window)

            plt.gca().set_prop_cycle(None)
            comp = list(pca.components_[0, :])
            for c in comp:
                plt.plot(i, c, marker="x")
            repair.iloc[i * window_size:(i+1)*window_size, :] = pd.DataFrame(pca.predict(X_window))
    plt.show()

    return {"repair": repair, "runtime": timer.get_time(), "n_components": n_components
        , "threshold": threshold, "type": alg_type  , "name" : f'RPCA({n_components},{round(threshold,2)},_window)'}


class Robust_PCA_estimator(BaseEstimator):
    def __init__(self, cols=[0], delta=0.01
                 , threshold=1
                 , n_components=1
                 , shift=0
                 , time=False
                 , eps=1e-8
                 , max_iter=300
                 , component_method="TruncatedSVD"
                 , interpolate_anomalies = True
                 ):
        self.interpolate_anomalies = interpolate_anomalies
        self.cols = cols
        self.threshold = threshold
        self.delta = delta
        self.n_components = n_components
        self.shift = shift
        self.time = time
        self.eps = eps
        self.max_iter = max_iter
        self.component_method = component_method

    def get_params(self, **kwargs):
        return {"delta": self.delta
            , "threshold": self.threshold
            , "n_components": self.n_components
            , "shift": self.shift
            , "time": self.time
            , "eps": self.eps
            , "max_iter": self.max_iter
            , "component_method": self.component_method
            , "interpolate_anomalies": self.interpolate_anomalies
            }

    # def score(self,y,X):
    #     print("yyyy",y)
    #     return 1

    def add_features(self, X):
        return pd.concat([X] + [X.shift(i, fill_value=0) for i in range(self.shift)], axis=1)

    def get_components(self, centered_weighted_x):
        n_components = min(centered_weighted_x.shape[1] - 1, self.n_components)
        if self.component_method == "fastICA":
            incPCA = FastICA(n_components=self.n_components)
            incPCA.fit(centered_weighted_x)
            components = incPCA.components_
            return components

        if self.component_method == "TruncatedSVD":
            tsvd = TruncatedSVD(n_components=n_components)
            tsvd.fit(centered_weighted_x)

            components = tsvd.components_
            return components

        U, S, V = linalg.svd(centered_weighted_x)
        components = V[:self.n_components, :]

        return components

    def fit(self, X, y=None):
        self.delta_half_square = (self.delta ** 2) / 2.
        self.vectorized_loss = self.vec_call #np.vectorize(self.call)
        self.vectorized_weights = np.vectorize(self.weight)

        if issparse(X):
            raise TypeError('MRobustPCA does not support sparse input.')

        col_n = X.shape[1]

        X = self.add_features(X)

        X = check_array(X, dtype=[np.float32], ensure_2d=True,
                        copy=True)

        n_samples, n_features = X.shape
        self.weights_ = 1. / n_samples * np.ones(n_samples)

        self.errors_ = [np.inf]
        self.n_iterations_ = 0
        not_done_yet = True

        while not_done_yet:
            # Calculating components with current weights

            self.mean_ = np.average(X, axis=0, weights=self.weights_)
            X_centered = X - self.mean_
            self.components_ = self.get_components(X_centered * np.sqrt(self.weights_.reshape(-1, 1)))

            # non_projected_metric = np.eye(self.components_.shape[1]) - \
            #                        self.components_.T.dot(self.components_)



            diff = X_centered - np.dot(X_centered, self.components_.T).dot(self.components_)
            diff = diff[:, :col_n]
            errors_raw = np.linalg.norm(diff, axis=1)

            errors_loss = self.vectorized_loss(errors_raw)
            # New weights based on errors
            self.weights_ = self.vectorized_weights(errors_raw)
            self.weights_ /= self.weights_.sum()
            # Checking stopping criteria
            self.n_iterations_ += 1
            old_total_error = self.errors_[-1]
            total_error = errors_loss.sum()

            if not np.equal(total_error, 0.):
                rel_error = abs(total_error - old_total_error) / abs(total_error)
            else:
                rel_error = 0.

            self.errors_.append(total_error)
            not_done_yet = rel_error > self.eps and self.n_iterations_ < self.max_iter

        self.components_ = self.components_[:col_n]
        return self

    def reduce(self, X):
        original_rows, original_cols = X.shape
        #X = self.add_features(X)
        X = self._validate_data(X, dtype=[np.float32], reset=False)
        if self.mean_ is not None:
            X = X - self.mean_
        X_transformed = np.dot(X, self.components_.T)
        X_reduced = np.dot(X_transformed, self.components_) + self.mean_

        return X_reduced[:, :original_cols]

    def classifiy_anomalies(self,X , reconstructed):
        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)

        # classify anomalies
        anomalies = {}
        for col in self.cols:
            reconstructed_col = np.array(reconstructed[:, col])
            diff = reconstructed_col - X_copy[:, col]
            mean = np.mean(diff)
            std = np.std(diff)
            abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
            to_repair_booleans = abs_z_score > self.threshold
            anomalies[col] = to_repair_booleans
            return anomalies

    def score(self,X,y):
        return -RMSE(pd.DataFrame(self.predict(X)),y,self.cols)

    def predict(self, X):
        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)
        X_reduced = self.reduce(X)

        anomalies = self.classifiy_anomalies(X,X_reduced)
        #replace
        if not self.interpolate_anomalies:
            assert False
        #     for col in self.cols:
        #         X_copy[anomalies[col],col] = reconstructed_col[anomalies[col]]

        #interpolate wrong values
        else:
            #interplate values in X where anomalies are
            interplated_df = X.copy()
            for col in self.cols:
                to_repair_booleans= anomalies[col].copy()
                to_repair_booleans[:3] = False
                to_repair_booleans[-3:] = False
                X_copy[to_repair_booleans, col] = np.nan
                interplated_df.iloc[:,col] = pd.Series(interplated_df.iloc[:,col]).interpolate(limit=200000,limit_area='inside')

                def print_series(df):
                    for i in range(len(df)):
                        print(df.iloc[i])
                assert not interplated_df.iloc[:,col].isnull().any().any() , f"nan found{print_series(pd.Series(X_copy[:,col]))} ,{print_series(pd.Series(X_copy[:,col]).interpolate(limit=200000,limit_area='inside'))}"

            #replace with the reduced data
            X_reduced = self.reduce(interplated_df)
            for col in self.cols:
                X_copy[anomalies[col], col] = X_reduced[anomalies[col],col]

        return X_copy

    def __main__(self):
        return self

    def vec_call(self,x):
        smaller = x <= self.delta
        bigger = np.invert(smaller)
        result = np.zeros_like(x)
        result[smaller] = x[smaller] ** 2 / 2.
        result[bigger] = self.delta * x[bigger] - self.delta_half_square
        return result

    def call(self, x):
        x_flt = float(x)
        assert x_flt >= 0
        if x_flt <= self.delta:
            return (x_flt ** 2) / 2.
        else:
            return self.delta * x_flt - self.delta_half_square

    def weight(self, x):
        x_flt = float(x)
        # assert x_flt >= 0
        if x_flt <= self.delta:
            return 1.0
        else:
            return self.delta / x_flt


