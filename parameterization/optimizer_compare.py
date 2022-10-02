import csv

import algorithms
from Injection.Scenarios.scen_gen import create_injected_DataContainer
from algorithms.estimator import Estimator

from parameterization.optimizers import EstimatorOptimizer, BayesianOptimizer
import algorithms.algorithms_config  as ac



def run_saved_optimization(estimator: Estimator, train_data,*,optimizer = None , param_grid = "infer",
                      save_folder="parameterization/parameterization_results",
                        ):

    if param_grid == "infer":
        param_grid = estimator.suggest_param_range(train_data.injected)

    optimizers = {
        "bayesian20": BayesianOptimizer(estimator, error_score, n_calls=20),
        "bayesian50": BayesianOptimizer(estimator, error_score, n_calls=50),
        "grid": EstimatorOptimizer(estimator, error_score)
    }

    result = {}
    for optimizer_name, optimizer in optimizers.items():
        result[optimizer_name] = optimizer.find_optimal_params(train_data.repair_inputs, param_grid)

    return result

a_type = "shift"
error_score = "full_rmse"


total_results = {}
for file_name in ["bafu", "humidity", "elec"]:
    total_results[file_name] = {}
    for estim_name in [ac.IMR]:  # , "screen" , "imr" , "cdrec"]:
        estimator: Estimator = algorithms.algo_mapper[estim_name]()
        train_container = create_injected_DataContainer(file_name, "train", a_type=a_type)
        optim_result = run_saved_optimization(estimator,train_container)
        total_results[estim_name] = optim_result