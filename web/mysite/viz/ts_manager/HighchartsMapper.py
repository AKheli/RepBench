import numpy as np
import pandas as pd
from pandas import DataFrame

from Injection.injected_data_part import InjectedDataContainer
from data_methods.data_class import DataContainer


## mapping to highcharts series
def map_truth_data(data_container: DataContainer, viz=5):
    df, df_norm = data_container.original_data, data_container.norm_data
    data = {
        'series': [{"visible": i < viz, "id": col_name, "name": col_name, "data": list(df[col_name])
                       , "norm_data": list(df_norm[col_name])} for (i, col_name)
                   in
                   enumerate(df.columns)]
    }
    return data


def map_injected_series(injected_series,col_name,data_container):
    #assume normalized data got injected

    col_mean = data_container.original_data[col_name].mean()
    col_std = data_container.original_data[col_name].std()
    data_norm = injected_series
    data =  data_norm * col_std + col_mean
    print(data_norm)
    print(data)
    injected_series = { "linkedTo": col_name,
                   "id": f"{col_name}_injected",
                   "name": f"{col_name}_injected",
                   "data": data.replace({np.nan: None}).values.tolist(),
                   "norm_data": data_norm.replace({np.nan: None}).values.tolist(),
                   "color": "red",
                   }
    return injected_series


def map_repair_data(repair: DataFrame, injected_data_container: InjectedDataContainer, alg_name: str,
                    repair_is_normalized=False):
    truth = injected_data_container.truth
    repair.columns = truth.columns
    injected_data_container: InjectedDataContainer
    data = {
        col_name + "repair": {"linkedTo": col_name,
                              "id": col_name + "repair",
                              "name": alg_name,
                              "data": list(repair[col_name]),
                              "norm_data": list(repair[col_name])
                              }
        for (i, col_name) in enumerate(injected_data_container.truth.columns) if
        i in injected_data_container.injected_columns}

    return data
