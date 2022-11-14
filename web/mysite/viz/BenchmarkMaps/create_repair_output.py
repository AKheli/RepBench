from data_methods import normalize_together
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from algorithms import algo_mapper


def generate_repaired_series_output(repair, injected_columns_index_map):
    """
       Returns:
       repaired_series = {
               's1': {'linkedTo': truth_series_id, (as provided by js from  the injected series)
                          'id': f"{col_name}_alg_type", (col_name provided by js)
                           'name': f"{col_name}_injected",
                           'data': repaired_column
                 },
                 's2:...
       """
    repaired_series = {}
    for col_name, col_index in injected_columns_index_map.items():
        repaired_series[col_name] = {
            'linkedTo': col_name,
            'id': col_index,
            'name': f"{col_name}_repaired",
            'data': repair.iloc[:, col_index].values.tolist(),
            'zIndex': -1
        }
    return repaired_series


def repair_from_None_series(alg_type,params, truth_df, *injected_series_dicts   ):
    injected_data_container = injected_container_None_Series(truth_df, *injected_series_dicts)
    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, params)

    repair = repair_info["repair"]
    scores = repair_info["scores"]

    error_map = { "rmse" :  "RMSE", "mae" : "MAE", "partial_rmse" : "RMSE on Anomaly" , "runtime" : "runtime"}
    data = {"data" : [{"name": error_map[k], "y": v} for k, v in scores.items() if  k in error_map.keys() ] }
    metrics = list(scores.keys())
    alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
    scores = {"name": alg_name, "colorByPoint": "true", "data": data}
    injected_columns_index_map = {isd["linkedTo"]: list(truth_df.columns).index(isd["linkedTo"]) for isd in
                                  injected_series_dicts}

    repaired_series = generate_repaired_series_output(repair, injected_columns_index_map)
    for v in repaired_series.values():
        v["name"] = alg_name
    return {"repaired_series": repaired_series, "scores": scores ,"metrics" : metrics}




from parameterization.optimizers.bayesian_optimization import BayesianOptimizer
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
