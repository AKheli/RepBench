from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series


def generate_repaired_series_out_put(repair, injected_columns_index_map):
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
    # todo
    for col_name, col_index in injected_columns_index_map.items():
        repaired_series[col_name] = {
            'linkedTo': col_name,
            'id': col_index,
            'name': f"{col_name}_repaired",
            'data': repair.iloc[:, col_index].values.tolist(),
            'zIndex': -1
        }
    return repaired_series


def repair_from_None_series(js_dict, truth_df, *injected_series_dicts):
    injected_data_container = injected_container_None_Series(truth_df, *injected_series_dicts)
    alg_type = js_dict.pop("alg_type")
    _ = js_dict.pop("csrfmiddlewaretoken")
    params = js_dict
    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, params)
    repair = repair_info["repair"]
    runtime = repair_info["runtime"]
    scores = repair_info["scores"]
    # series: [
    #     {
    #         name: "Browsers",
    #         colorByPoint: true,
    #         data: [
    #             {
    #                 name: "Chrome",
    #                 y: 63.06,
    #                 drilldown: "Chrome"
    #             },
    #             {
    data = [{"name": k, "y": v} for k, v in scores.items()]
    metrics = list(scores.keys())
    alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
    scores = {"name": alg_name, "colorByPoint": "true", "data": data}
    injected_columns_index_map = {isd["linkedTo"]: list(truth_df.columns).index(isd["linkedTo"]) for isd in
                                  injected_series_dicts}

    repaired_series = generate_repaired_series_out_put(repair, injected_columns_index_map)
    for v in repaired_series.values():
        v["name"] = alg_name
    return {"repaired_series": repaired_series, "scores": scores ,"metrics" : metrics}
