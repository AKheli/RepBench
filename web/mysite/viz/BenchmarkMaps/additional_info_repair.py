from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series


def repair_from_None_series_with_additional_info(alg_type,params, truth_df, *injected_series_dicts   ):
    injected_data_container = injected_container_None_Series(truth_df, *injected_series_dicts)
    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, params,additional_context=True)

    repair = repair_info["repair"]
    scores = repair_info["scores"]
    additional_repair_info = repair_info["additional_results"]

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
    return {"repaired_series": repaired_series, "scores": scores ,"metrics" : metrics , "additional_repair_info" : additional_repair_info}




