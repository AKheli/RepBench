from algorithms import algo_mapper
from parameterization.optimizers import BayesianOptimizer
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.create_repair_output import generate_repaired_series_output
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series


def optimize_from_None_series(param_ranges,alg_type,bayesian_opt_inputs,truth_df, *injected_series_dicts):
    injected_data_container = injected_container_None_Series(truth_df, *injected_series_dicts)
    estimator = algo_mapper[alg_type]()
    optimizer = BayesianOptimizer(estimator,**bayesian_opt_inputs,n_restarts_optimizer=1)
    params, scores = optimizer.search(injected_data_container.repair_inputs,param_ranges,return_full_minimize_result=True)

    min_index = list(scores).index(min(scores))
    optimal_params = params[min_index]

    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, optimal_params)
    repair = repair_info["repair"]
    injected_columns_index_map = {isd["linkedTo"]: list(truth_df.columns).index(isd["linkedTo"]) for isd in
                                  injected_series_dicts}

    repaired_series = generate_repaired_series_output(repair, injected_columns_index_map)

    data =  {"name": alg_type , "data" :[ {"name" : str(param) , "y" :  float(score) }for param,score in zip(params,scores)]}
    return {"opt_result_series": data , "metric" : "full_rmse" , "optimal_params" : optimal_params , "repaired_series" : repaired_series}
