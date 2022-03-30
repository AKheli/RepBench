import pandas as pd
from matplotlib import pyplot as plt

from Repair.Dimensionality_Reduction.CDrec.recovery import interpolate
from Repair.Dimensionality_Reduction.RobustPCA.reduction import fit_components
from Repair.Dimensionality_Reduction.difference_classifier import difference_classify
from Repair.estimator import estimator
import numpy as np

class Robust_PCA_estimator(estimator):

    def __init__(self, n_components=1
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
        self.n_components = n_components
        self.eps = eps
        self.max_iter = max_iter
        self.alg_type = "RPCA"
        super().__init__(**kwargs)

    def suggest_param_range(self,X):
        #todo smin and smax suggestion
        return {"n_components" : list(range(1,X.shape[1])),
                "delta" : np.logspace(0,1,num = 100),
                "threshold" : np.linspace(0,1,num = 50)}



    def reduce(self, matrix):
        matrix = matrix.copy()
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        self.C , self.mean , self.weights = fit_components(matrix*1, self.n_components, self.delta , max_iter  = self.max_iter)
        reduced =  np.dot(matrix-self.mean, self.C.T).dot(self.C) + self.mean

        return reduced

    def _fit(self,X,y=None):
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

        # i = 0
        # for ax , d in zip(plt.subplots(4,figsize=(60, 60))[1],[matrix,reduced,repair,matrix_inter]):
        #     ax.plot(d)
        #     ax.set_title(str(i))
        #     i += 1
        # plt.title(str(self.C))
        #
        # plt.show()
        # plt.plot(anomaly_matrix)
        # plt.show()

        return repair

    def classify(self, matrix , reduced = None):
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        if reduced is None:
            reduced = self.reduce(matrix)
        assert matrix.shape == reduced.shape
        diff = matrix - reduced
        anomaly_matrix = difference_classify(diff, self.threshold,self.cols)
        return anomaly_matrix

    ## add fit() for train and check if it is fitted on predict and reduce

    # def repair(self, matrix, anomaly_matrix=None):
    #     if isinstance(matrix, pd.DataFrame):
    #         matrix = matrix.values
    #
    #     reduced = self.reduce(matrix)
    #     if anomaly_matrix is None:
    #         anomaly_matrix = self.classify(matrix,reduced=reduced)
    #
    #     assert matrix.shape == anomaly_matrix.shape
    #
    #     repair = matrix.copy()
    #
    #     if self.interpolate_anomalies:
    #         matrix_to_interpolate = matrix.copy()
    #         print(anomaly_matrix)
    #         matrix_to_interpolate[anomaly_matrix] = np.nan
    #         matrix = interpolate(matrix_to_interpolate,anomaly_matrix)
    #         reduced = self.reduce(matrix)
    #         repair[anomaly_matrix] = reduced[anomaly_matrix]
    #
    #     else:
    #         reduced = self.reduce(matrix)
    #         repair[anomaly_matrix] = reduced[anomaly_matrix]
    #
    #     return repair

    def algo_name(self):
        return f'RPCA({self.n_components},{self.delta},{round(self.threshold,2)})'