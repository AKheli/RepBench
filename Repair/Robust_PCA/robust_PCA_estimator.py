import warnings

import numpy as np
from scipy import linalg
from scipy.sparse import issparse
from sklearn.utils import check_array
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import FastICA

from ParameterTuning.EM_bootstrap import in_interval, conf_interval
from Repair.estimator import estimator
import time
warnings.simplefilter("ignore", UserWarning)  # feaure name

class Robust_PCA_estimator(estimator):
    def __init__(self, n_components =2,
                 cols=[0]
                 , delta=0.01
                 , threshold=10
                 , infer_threshold = True
                 , eps=1e-8
                 , max_iter=300
                 , component_method="TruncatedSVD"
                 , interpolate_anomalies = True
                 , fit_on_truth = True
                 , threshold_boundaries = (0.1,4)
                 , **kwargs
                 ):
        self.threshold = threshold
        self.infer_threshold = infer_threshold
        #self.best_threshold = None
        self.threshold_boundaries = threshold_boundaries
        self.fit_on_truth = fit_on_truth
        self.interpolate_anomalies = interpolate_anomalies
        self.cols = cols
        self.delta = delta
        self.n_components = n_components
        self.eps = eps
        self.max_iter = max_iter
        self.component_method = component_method
        self.times = {}
        super().__init__(**kwargs)


    def get_params(self, **kwargs):
        return {"delta": self.delta
            , "threshold": self.threshold
            , "n_components": self.n_components
            , "component_method": self.component_method
            , "interpolate_anomalies": self.interpolate_anomalies
            , "fit_on_truth" : self.fit_on_truth
            , "infer_threshold" : self.infer_threshold
            }

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

        self.delta_half_square = (self.delta ** 2) / 2.
        self.vectorized_loss = self.vec_call
        self.vectorized_weights = np.vectorize(self.weight)

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

            errors_raw = np.linalg.norm(diff, axis=1)

            errors_loss = self.vectorized_loss(errors_raw)
            # New weights based on errors
            self.weights_ += self.vectorized_weights(errors_raw)
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

        if y is not None and self.infer_threshold:
            self.set_threshold_on_current_settings(X,y)
        return self

    def f(self, t, X, y):
        self.threshold = t
        return -self.score(X.copy(), y.copy())

    def set_threshold_on_current_settings(self,X,y):
        assert self.infer_threshold

        x = self.threshold_boundaries
        to_minize = lambda t : self.f(t, X, y)

        minscore =  np.inf
        minimum_t = x[0]
        maximum_t = x[1]
        results = []
        for i in np.linspace(x[0],x[1]):
            val = to_minize(i)
            results.append((i,val))
            if np.isclose(val,minscore,atol=1e-07):
                if i < minimum_t:
                    minimum_t = i
                if i > maximum_t:
                    maximum_t = i
            elif val < minscore:
                minimum_t = i
                maximum_t = i
                minscore = val
        self.threshold = (minimum_t+maximum_t)/2

    def reduce(self, X):
        original_rows, original_cols = X.shape
        #X = self.add_features(X)
        X = self._validate_data(X, dtype=[np.float32], reset=False)
        if self.mean_ is not None:
            X = X - self.mean_
        X_transformed = np.dot(X, self.components_.T)
        X_reduced = np.dot(X_transformed, self.components_) + self.mean_

        return X_reduced[:, :original_cols]

    def get_fitted_attributes(self):
        "dict of fitted atributes"
        return {"threshold" : self.threshold , "components" : self.components_.copy()  }

    def merge_fitted_attributes(self, list_of_fit_results,anomaly_vector_list = None):
        assert False
        super().merge_fitted_attributes(list_of_fit_results,anomaly_vector_list)

        weights = np.ones(len(list_of_fit_results))
        weights = weights/len(weights)
        if anomaly_vector_list is not None:
            sums = np.array([ sum(anoms) for anoms in  anomaly_vector_list])
            weights = sums/sum(sums)

        assert np.isclose(sum(weights),1)

        self.threshold =  sum([ d["threshold"]*w for w,d in zip(weights,list_of_fit_results)])
        self.components_ =  np.sum( [d["components"] for d in list_of_fit_results ] ,axis = 1 )/len(list_of_fit_results)

    def classify_anomalies(self, X, reconstructed):
        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)

        # classify anomalies
        anomalies = {}
        for col in self.cols:
            reconstructed_col = np.array(reconstructed[:, col])
            to_repair_booleans = np.zeros_like(reconstructed_col,dtype=bool)

            diff = abs(reconstructed_col - X_copy[:, col])
            mean = np.mean(diff)
            std = np.std(diff)

            for i in range(10,len(to_repair_booleans)-1):
                to_repair_booleans[i]= (1+0*sum(to_repair_booleans[i-2:i-1]))*(diff[i]-mean)/std > self.threshold

            self.lower = reconstructed_col - (self.threshold*std+mean)
            self.upper = reconstructed_col + (self.threshold*std+mean)

            anomalies[col] = to_repair_booleans
            return anomalies


    def _predict(self, X):
        X = X.copy()
        X_copy = self._validate_data(X, dtype=[np.float32], reset=False)
        X_reduced = self.reduce(X)

        anomalies = self.classify_anomalies(X, X_reduced)

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

