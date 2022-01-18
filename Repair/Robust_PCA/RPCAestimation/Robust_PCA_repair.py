import numpy as np
import pandas as pd
import sklearn
from matplotlib import pyplot as plt
from scipy import linalg
from scipy.sparse import issparse
from sklearn.base import BaseEstimator
from sklearn.utils import check_array
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import FastICA
from skopt import gp_minimize, dummy_minimize

from ParameterTuning.EM_bootstrap import in_interval, conf_interval
from Repair.Algorithms_File import RPCA, ALGORITHM_PARAMETERS
from Repair.estimator import estimator
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




import time

class Robust_PCA_estimator(estimator):
    def __init__(self, cols=[0], delta=0.01
                 , threshold=1
                 , n_components=1
                 , shift=0
                 , time=False
                 , eps=1e-8
                 , max_iter=300
                 , component_method="TruncatedSVD"
                 , interpolate_anomalies = True
                 , fit_on_truth = True
                 , threshold_boundaries = (0.5,4)
                 , **kwargs
                 ):
        self.best_threshold = None
        self.threshold_boundaries = threshold_boundaries
        self.fit_on_truth = fit_on_truth
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
        self.times = {}
        estimator.__init__(self)


    def get_params(self, **kwargs):
        return {"delta": self.delta
            , "threshold": self.threshold
            , "n_components": self.n_components
            , "component_method": self.component_method
            , "interpolate_anomalies": self.interpolate_anomalies
            , "fit_on_truth" : self.fit_on_truth
            , "best_threshold" : self.best_threshold
            }

    # def score(self,y,X):
    #     print("yyyy",y)
    #     return 1

    # def add_features(self, X):
    #     return pd.concat([X] + [X.shift(i, fill_value=0) for i in range(self.shift)], axis=1)

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

    def _fit(self, X, y=None):
        # if y is not None and self.fit_on_truth:
        #     X = y
        self.delta_half_square = (self.delta ** 2) / 2.
        self.vectorized_loss = self.vec_call #np.vectorize(self.call)
        self.vectorized_weights = np.vectorize(self.weight)

        if issparse(X):
            raise TypeError('MRobustPCA does not support sparse input.')

        col_n = X.shape[1]

        X = check_array(X, dtype=[np.float32], ensure_2d=True,
                        copy=True)

        n_samples, n_features = X.shape
        self.weights_ = 1. / n_samples * np.ones(n_samples)

        self.errors_ = [np.inf]
        self.n_iterations_ = 0
        not_done_yet = True
        t  = time.time()
        while not_done_yet:
            # Calculating components with current weights
            if time.time() - t > 5:
                print("rpca_iters" , self.n_iterations_)
                t = time.time()

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

        if y is not None:
            self.set_threshold_on_current_settings(X,y)
        return self

    def f(self, t, X, y):
        #print("TTTTTTTTTTTT",self.best_threshold)
        #print(t)
        self.best_threshold = t
        return -self.score(X.copy(), y.copy())

    def set_threshold_on_current_settings(self,X,y):
        x = self.threshold_boundaries
        to_minize = lambda t : self.f(t, X, y)

        minscore =  np.inf
        minimum_t = x[0]
        maximum_t = x[1]
        results = []
        for i in np.linspace(x[0],x[1]):
            val = to_minize(i)
            results.append((i,val))
            if np.isclose(val,minscore,atol=1e-08):
                if i < minimum_t:
                    minimum_t = i
                if i > maximum_t:
                    maximum_t = i
            elif val < minscore:
                minimum_t = i
                maximum_t = i
                minscore = val
        # r = dummy_minimize( lambda t : self.f(t, X, y)
        # , x, n_calls=30, verbose=True)
        #
        # r.x_iters #  location of function evaluation for each iteration
        # func_vals #
        # print("TTTTTTTTTTT" , minimum_t , maximum_t , to_minize(minimum_t) , to_minize(maximum_t) ,to_minize(minimum_t-0-5))
        # print(results)
        self.best_threshold = (minimum_t+maximum_t)/2#, n_initial_points=30,  n_restarts_optimizer=1, n_points=200, acq_func='EI').x[0]

    def reduce(self, X):
        original_rows, original_cols = X.shape
        #X = self.add_features(X)
        X = self._validate_data(X, dtype=[np.float32], reset=False)
        if self.mean_ is not None:
            X = X - self.mean_
        X_transformed = np.dot(X, self.components_.T)
        X_reduced = np.dot(X_transformed, self.components_) + self.mean_

        return X_reduced[:, :original_cols]

    def classify_anomalies(self, X, reconstructed):
        if self.best_threshold is None:
            self.best_threshold = self.threshold

        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)

        # classify anomalies
        anomalies = {}
        for col in self.cols:
            reconstructed_col = np.array(reconstructed[:, col])
            to_repair_booleans = np.zeros_like(reconstructed_col,dtype=bool)

            #pca = sklearn.decomposition.PCA(n_components=self.n_components)
            #self.pca = pca.inverse_transform(pca.fit_transform(X_copy))[:,col]
            diff = abs(reconstructed_col - X_copy[:, col])
            mean = np.mean(diff)
            std = np.std(diff)
            # abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)
            # to_repair_booleans = abs_z_score > self.threshold
            for i in range(10,len(to_repair_booleans)-1):
                to_repair_booleans[i]= (1+0*sum(to_repair_booleans[i-2:i-1]))*(diff[i]-mean)/std > self.best_threshold

            self.lower = reconstructed_col - (self.best_threshold*std+mean)
            self.upper = reconstructed_col + (self.best_threshold*std+mean)

            #did not work
            #to_repair_booleans = self.in_interval(X_copy[:, col],reconstructed_col,self.threshold)
            anomalies[col] = to_repair_booleans
            #print("CLAAAS SUUUM" , sum(to_repair_booleans))
            return anomalies

    def in_interval(self, injected, reduced, alpha, samples=100):
        injected = injected.copy()
        reduced = np.array(reduced)
        assert reduced.ndim == 1
        lower, upper = conf_interval(injected, alpha, samples)
        self.lower = lower
        self.upper = upper
        to_repair_values = np.logical_or(reduced < lower, reduced > upper)
        # print(to_repair_values)
        return to_repair_values

    def _predict(self, X):
        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)
        X_reduced = self.reduce(X)

        anomalies = self.classify_anomalies(X, X_reduced)
        #replace

        #     for col in self.cols:
        #         X_copycopy()[anomalies[col],col] = reconstructed_col[anomalies[col]]


        to_reduce = np.array(X).copy()
        if self.interpolate_anomalies:
            for col in self.cols:
                to_repair_booleans= anomalies[col].copy()
                i = 1
                while i < len(to_repair_booleans):
                    if to_repair_booleans[i]:
                        last_clean_pont = i-1
                        while to_repair_booleans[i]:
                            i = i+1
                        next_clean_pont = i
                        to_reduce[last_clean_pont+1:next_clean_pont ,col] \
                            = np.linspace(to_reduce[last_clean_pont,col],to_reduce[next_clean_pont,col],next_clean_pont-last_clean_pont-1)
                    else:
                        i = i+1
                        #anomaly_found



        #replace with the reduced data
        X_reduced = self.reduce(to_reduce)
        for col in self.cols:
            reduced_col = X_reduced[:,col]
            self.reduced = reduced_col
            X_copy[anomalies[col], col] = reduced_col[anomalies[col]]

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


