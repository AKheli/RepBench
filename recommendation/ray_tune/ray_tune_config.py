import numpy as np
from ray import tune



RAYTUNE_ESTIMATORS = ["RandomForest", "LGBM", "ExtraTrees", "LogisticRegression"]


config = {
    "model": tune.choice([RAYTUNE_ESTIMATORS]),
    "n_estimators": tune.randint(5, 30),
    "max_depth": tune.randint(3, 10),
    "min_samples_split": tune.randint(2, 6),
    "num_leaves": tune.randint(2, 30),
    "learning_rate": tune.choice(np.logspace(-4,0, 500)),
    "min_child_samples": tune.randint(3, 15),
    "C": tune.choice(np.logspace(-5,0, 500)) ,#tune.loguniform(1e-3, 1)
    "max_features" : tune.randint(3, 30),
    "max_leaf_nodes" : tune.randint(3, 20),
}


#
# config = {
#     "model": tune.choice(["RandomForest", "LGBM", "ExtraTrees", "LogisticRegression"]),
#     "n_estimators": tune.randint(5, 30),
#     "max_depth": tune.randint(3, 10),
#     "min_samples_split": tune.randint(2, 6),
#     "num_leaves": tune.randint(4, 20),
#     "learning_rate": tune.loguniform(1e-3, 1),
#     "min_child_samples": tune.randint(3, 15),
#     "C": tune.loguniform(1e-3, 1)
# }