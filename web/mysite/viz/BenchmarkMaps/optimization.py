from Injection.injected_data_part import InjectedDataContainer
from algorithms import algo_mapper
from parameterization.optimizers import BayesianOptimizer
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.ts_manager.ts_manager import get_repair_data


def optimize_web(param_ranges, alg_type, injected_data_container : InjectedDataContainer, *, error_loss, n_calls, n_initial_points,callback=None):
    estimator = algo_mapper[alg_type]()


    optimizer = BayesianOptimizer(estimator,error_score=error_loss,n_calls=n_calls,n_initial_points=n_initial_points,n_restarts_optimizer=1,callback=callback)
    params, scores = optimizer.search(injected_data_container.repair_inputs,param_ranges,return_full_minimize_result=True)

    min_index = list(scores).index(min(scores))
    optimal_params = params[min_index]

    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, optimal_params)
    repair = repair_info["repair"]

    repaired_series = get_repair_data(repair, injected_data_container,alg_type)

    data =  {"alg_type": alg_type ,
             "data" :[ {"name" : dict(param) , "y" :  float(score) }for param,score in zip(params,scores)],
             "error_loss" : error_loss,
             "n_calls" : n_calls,
             "n_initial_points" :  n_initial_points,
             "repaired_series": repaired_series,
             "optimal_params": optimal_params
             }

    return data
