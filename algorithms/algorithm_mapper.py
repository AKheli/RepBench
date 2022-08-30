import algorithms as algs
import algorithms.algorithms_config as ac

algo_mapper = {
    ac.CDREC: algs.CDRecEstimator,
    ac.RPCA: algs.Robust_PCA_estimator,
    ac.SCREEN: algs.SCREENEstimator,
    ac.IMR: algs.IMR_estimator
}
