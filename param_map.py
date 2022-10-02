import numpy as np
import os
from itertools import product

import algorithms
import algorithms.algorithms_config  as ac
from Injection.Scenarios.scen_gen import create_injected_DataContainer
from algorithms.estimator import Estimator
from parameterization.optimizers import EstimatorOptimizer, BayesianOptimizer
import json

error_scores = ["full_rmse","partial_rmse","mae"]
a_types = ["shift","outlier","distortion"]
estim_names =[ac.IMR,ac.SCREEN,ac.Robust_PCA,ac.CDREC,ac.SCREEN_GLOBAL]

error_score = "full_rmse"
a_type = "shift"
total_results = {}
estim_name = ac.SCREEN

try:
    os.mkdir("parameterization/parameterization_results")
except:
    pass

for a_type,error_score,estim_name in list(product(a_types,error_scores,estim_names)):
    store_file_name = f"{estim_name}_{a_type}_{error_score}"
    print(store_file_name)
    for file_name in ["bafu"]:#, "humidity", "elec" , "msd"]:
            estimator : Estimator = algorithms.algo_mapper[estim_name]()
            train_container = create_injected_DataContainer(file_name, "train", a_type=a_type)
            param_grid = estimator.suggest_param_range(train_container.injected)
            optimizer = EstimatorOptimizer(estimator, error_score)
            results = optimizer.param_map(train_container.repair_inputs,param_grid)

            optimizer =  BayesianOptimizer(estimator, error_score)
            bayesian_opt_scores =   optimizer.find_optimal_params(train_container.repair_inputs,param_grid)
            total_results[file_name] = [{"bayesian_opt_scores":bayesian_opt_scores }]+results+[{"param_grid":{k:list(v) for k,v in param_grid.items()}}]


    with open(f"parameterization/parameterization_results/{store_file_name}.json", "w") as outfile:
        print(total_results)


        def default(obj):
            if isinstance(obj,(np.int64)):
                return int(obj)

            if isinstance(obj,np.float64):
                return float(object)

            return obj
        
        json.dump(total_results, outfile,default=default)
