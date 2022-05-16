import pandas as pd
from Repair.Dimensionality_Reduction.Dimensionality_Reduction_Estimator import DimensionalityReductionEstimator
import numpy as np
from scipy import linalg
from sklearn.decomposition import TruncatedSVD

from Repair.algorithms_config import RPCA


class Robust_PCA_estimator(DimensionalityReductionEstimator):

    def __str__(self):
        return f'RPCA({self.classification_truncation},{self.repair_truncation},{self.delta},{round(self.threshold,2) , self.repair_iter , self.n_max_iter})'

    def compute_transform(self,centered_weighted_x, n_components, component_method="TruncatedSVD"):
        if component_method == "TruncatedSVD":
            tsvd = TruncatedSVD(n_components=n_components)
            tsvd.fit(centered_weighted_x)
            V = tsvd.components_
        else:
            U, S, V = linalg.svd(centered_weighted_x)
        biggest_eigen_vec = V[:n_components, :]
        return np.dot(biggest_eigen_vec.T,biggest_eigen_vec)

    @property
    def alg_type(self):
        name = RPCA
        return name