import Repair.algorithms_config as ac
from Repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.screen_estimator import SCREENEstimator

from parameter_search.estimator_optimizer import EstimatorOptimizer
from parameter_search.succesivehalving_search import SuccessiveHalvingOptimizer
from parameter_search.bayesian_optimization import BayesianOptimizer


def init_estimator_from_type(alg_type, params):
    params = {} if params is None else params
    estimator = None
    if alg_type in (ac.IMR, "imr"):
        estimator = IMR_estimator(**params)
    if alg_type in (ac.SCREEN, "screen"):
        estimator = SCREENEstimator(**params)
    if alg_type in (ac.RPCA, "rpca"):
        estimator = Robust_PCA_estimator(**params)
    if alg_type in (ac.CDREC, "cdrec"):
        estimator = CDRecEstimator(**params)
    assert estimator is not None, f'{alg_type} could not be parsed'

    return estimator