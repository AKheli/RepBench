import flaml
import pandas as pd

config_search_space = {
    "repair_truncation": flaml.tune.choice([2, 3, 4, 5]),
    "threshold": flaml.tune.loguniform(1.0, 3.0),
    "repair_iter": flaml.tune.choice([1, 10]),
    "n_max_iter": flaml.tune.choice([1, 20]),
    "classification_truncation": flaml.tune.choice([1, 2, 3, 4, 5]),
    "delta": flaml.tune.loguniform(1.5, 3.0),
}

# load injected Dataset
from injection import inject_data_df
from injection.injection_config import AMPLITUDE_SHIFT, POINT_OUTLIER
from algorithms.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from algorithms.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator

# load injected Dataset
truth_df = pd.read_csv("data/test/bafu5k.csv")
injected_df, _ = inject_data_df(truth_df, a_type=AMPLITUDE_SHIFT)


def evaluate_config(config: dict):
    rmse = CDRecEstimator(**config).scores(injected_df, truth_df, [0], None)["rmse"]
    print(rmse)
    return rmse


analysis = flaml.tune.run(
    evaluate_config,  # the function to evaluate a config
    config=config_search_space,  # the search space defined
    mode="min",  # the optimization mode, "min" or "max"
    num_samples=50,  # the maximal number of configs to try, -1 means infinite
    time_budget_s=500,  # the time budget in seconds
)
