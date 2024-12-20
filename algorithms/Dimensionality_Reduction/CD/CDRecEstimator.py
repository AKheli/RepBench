import time

from repair.Dimensionality_Reduction.CD.sign_vector_computations import *
from repair.algorithms_config import CDREP
from repair.Dimensionality_Reduction.dimensionality_reduction_estimator import DimensionalityReductionEstimator
import numpy as np


class CDRecEstimator(DimensionalityReductionEstimator):

    def __init__(self, classification_truncation=2, repair_truncation=None,
                 delta=1.5, t=1, eps=1e-6, n_max_iter=1, repair_iter=10,
                 k=None, threshold=None, **kwargs):
        super().__init__(classification_truncation, repair_truncation, delta, t,
                         eps, n_max_iter, repair_iter, k, threshold, **kwargs)

    def compute_transform(self, centered_weighted_x, truncation, component_method=None):
        L, R, Z = weighted_centroid_decomposition(centered_weighted_x , truncation=truncation, weights=None)
        return np.dot(R,R.T)

    @property
    def alg_type(self):
        return CDREP

    def __str__(self):
        if self.n_max_iter < 2:
            return f'CDrec({self.classification_truncation},{self.repair_truncation},{self.delta},{round(self.threshold, 2), self.repair_iter})'

        return f'weighted_CDrec({self.classification_truncation},{self.repair_truncation},{self.delta},{round(self.threshold,2), self.repair_iter})'

def weighted_centroid_decomposition(matrix, truncation=0, weights = None , SV=None ):
    # input processing
    matrix = np.asarray(matrix, dtype=np.float64).copy()
    n = len(matrix)
    m = len(matrix[0])

    if truncation == 0:
        truncation = m

    if truncation < 1 or truncation > m:
        print("[Centroid Decomposition] Error: invalid truncation parameter k=" + str(truncation))
        print("[Centroid Decomposition] Aboritng decomposition")
        return None

    if SV is None:
        SV = default_SV(n, truncation)

    if len(SV) != truncation:
        print(
            "[Centroid Decomposition] Error: provided list of Sign Vectors doesn't match in size with the truncation truncation parameter k=" + str(
                truncation))
        print("[Centroid Decomposition] Aboritng decomposition")
        return None

    L = np.zeros((truncation, n))
    R = np.zeros((truncation, m))
    if weights is not None:
        matrix = matrix * np.sqrt(weights.reshape(-1, 1))

    # main loop - goes up till the truncation param (maximum of which is the # of columns)
    for j in range(0, truncation):
        # calculate the sign vector
        #Z = local_sign_vector(matrix, SV[j])
        Z = local_sign_vector_speed_up(matrix,SV[j])
        # calculate the column of R by X^T * Z / ||X^T * Z||
        R_i =  matrix.T @ Z
        R_i = R_i / np.linalg.norm(R_i)
        R[j] = R_i

        # calculate the column of L by X * R_i
        L_i = matrix @ R_i
        L[j] = L_i

        # subtract the dimension generated by L_i and R_i from the original matrix
        matrix = matrix - np.outer(L_i, R_i)

        # update the new sign vector in the array
        SV[j] = Z
    # end for

    return (L.T, R.T, SV)


