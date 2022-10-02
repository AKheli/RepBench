import algorithms as algs
import algorithms.algorithms_config as ac
import functools

algo_mapper = {
    ac.CDREC: algs.CDRecEstimator,
    ac.RPCA: algs.Robust_PCA_estimator,
    ac.SCREEN: algs.SCREENEstimator,
    ac.IMR: algs.IMR_estimator,
    ac.WindowRPCA: functools.partial(algs.Robust_PCA_estimator,windows = True),
    ac.SCREEN_GLOBAL : functools.partial(algs.SCREENEstimator,method = "global"),
}


