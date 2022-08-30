import csv

import algorithms
from Scenarios.data_generation import full_train_test
from Scenarios.data_part import DataPart
from algorithms.estimator import Estimator

from optimizers import (
    EstimatorOptimizer,
    BayesianOptimizer
)
from parameterization.optimizers.succesivehalving_search import SuccessiveHalvingOptimizer


def run_saved_optimization( optimizers : dict , estimator , a_type , data_set  ,error_score ,save_folder = "parameterization/parameterization_results"):
    file_name = f"{estimator.alg_type}_{error_score}_{data_set}_{a_type}"
    train_data : DataPart = full_train_test(data_set=data_set , a_type=a_type)[0]
    param_grid = estimator.suggest_param_range(train_data.injected)
    with open(f"{save_folder}/{file_name}" , 'w') as f:
        f.write("paramgrid: \n" + str(param_grid))
        f.write("\n")
        fieldnames = ['optimizer', 'parameters' , 'score' , 'time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for optimier_name , optimizer in optimizers.items():
            params , time, score = optimizer.find_optimal_params(train_data.repair_inputs , param_grid)
            writer.writerow({'optimizer': optimier_name, 'parameters': params, 'score' : score , 'time' : time})



a_type = "shift"
error_score = "full_rmse"

for data_set in ["bafu" , "humidity" , "elec"]:
    for estim_name in ["rpca" , "screen" , "imr" , "cdrec"]:
        estimator: Estimator = algorithms.algo_mapper[estim_name]()
        optimizers = {
                    "bayesian20": BayesianOptimizer(estimator, error_score, n_calls=20),
                     "bayesian50": BayesianOptimizer(estimator, error_score, n_calls=50),
                    "grid": EstimatorOptimizer(estimator, error_score),
                    "succesive" : SuccessiveHalvingOptimizer(estimator, error_score)
        }
        run_saved_optimization(optimizers, estimator, a_type, data_set, error_score=error_score)