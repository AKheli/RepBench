import pandas as pd
from matplotlib import pyplot as plt

from Repair.Dimensionality_Reduction.CDrec.recovery import interpolate
from Repair.Dimensionality_Reduction.Dimensionality_Reduction_Estimator import DimensionalityReductionEstimator
from Repair.Dimensionality_Reduction.RobustPCA.reduction import fit_components
from Repair.estimator import estimator
import numpy as np


class Robust_PCA_estimator(DimensionalityReductionEstimator):

    def _reduce(self, matrix, truncation):
        matrix = matrix.copy()
        if isinstance(matrix, pd.DataFrame):
            matrix = matrix.values

        self.C, self.mean, self.weights = fit_components(matrix * 1, truncation, self.delta, max_iter=self.max_iter)
        reduced = np.dot(matrix - self.mean, self.C.T).dot(self.C) + self.mean

        return reduced

    @property
    def alg_type(self):
        return "RPCA"

    def algo_name(self):
        return f'RPCA({self.repair_truncation},{self.classification_truncation},{self.delta},{round(self.threshold,2)})'
