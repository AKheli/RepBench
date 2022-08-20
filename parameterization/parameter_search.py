import sys ,os
print(sys.path)
sys.path.append(os.getcwd())
from Scenarios.data_part import DataPart
from Scenarios.scenario_generator import build_scenario
from parameterization.bayesian_optimization import BayesianOptimizer
from parameterization.estimator_optimizer import EstimatorOptimizer
from parameterization.succesivehalving_search import SuccessiveHalvingOptimizer
from testing_frame_work.estimator_init import init_estimator_from_type

TRAIN_METHODS = ["grid","bayesian" , "halving"]
optimizers_constr = {"grid": EstimatorOptimizer,
                    "halving": SuccessiveHalvingOptimizer,
                    "bayesian": BayesianOptimizer}

alg_type = "rpca"
search_type = "grid"

def try_params(alg_type, metric,train_method,repair_inputs, param_grid=None):
    estimator = init_estimator_from_type(alg_type,params= None)
    if param_grid is None:
        param_grid = estimator.suggest_param_range(repair_inputs["injected"])
    estimator_optimizer = optimizers_constr[train_method](estimator, metric)

    optimal_params , search_time = estimator_optimizer.find_optimal_params(repair_inputs, param_grid)
    return optimal_params , search_time




data = {}
for data_set in ["bafu","msd1_5","elec","humidity"]:
    data[data_set] = {}
    for a_type in ["shift", "distortion", "point"]:
        data[data_set][a_type] = {}
        screnario = build_scenario("base", data_set, a_type="shift",max_n_rows=5000)
        for key,val in screnario.part_scenarios.items():
            test_part : DataPart = val
            train_part : DataPart = test_part.train

        #print(test_part.injected)
        estimator = init_estimator_from_type(alg_type, params=None)
        param_grid = estimator.suggest_param_range(train_part.repair_inputs["injected"])

        for error_score in ["full_rmse","partial_rmse"]:
            data[data_set][a_type][error_score] = {}
            optimal_params , search_time = try_params(alg_type,error_score, search_type, train_part.repair_inputs)
            estimator.__dict__.update(optimal_params)
            score = estimator.scores(**train_part.repair_inputs)[error_score]
            score_test = estimator.scores(**test_part.repair_inputs)[error_score]

            data[data_set][a_type][error_score].update({"opt_params":optimal_params,"score":score,"time":search_time,"test_score" : score_test})

import toml
with open(f"parameterization/{alg_type}_{search_type}", "w") as toml_file:
    toml.dump(data, toml_file)



