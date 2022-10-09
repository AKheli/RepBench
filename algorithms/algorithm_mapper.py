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
    ac.SCREEN_l : functools.partial(algs.SCREENEstimator,ci = (5,95)),
    ac.SCREEN_l2 : functools.partial(algs.SCREENEstimator,ci = (10,90))
}


