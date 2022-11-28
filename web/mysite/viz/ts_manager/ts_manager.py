import numpy as np
import pandas as pd
from pandas import DataFrame

from Injection.injected_data_part import InjectedDataContainer
from data_methods.data_class import DataContainer


def load_data_set(setname, type="train"):
    container = DataContainer(setname)
    return container.original_data, container.norm_data


## mapping to highcharts series
def get_truth_data(setname="bafu5k", viz=5, type="train"):
    df, df_norm = load_data_set(setname, type=type)
    data = {
        'series': [{"visible": i < viz, "id": col_name, "name": col_name, "data": list(df[col_name])
                       , "norm_data": list(df_norm[col_name])} for (i, col_name)
                   in
                   enumerate(df.columns)]
    }
    return data


def get_injected_data(injected_data_container):
    injected_data_container: InjectedDataContainer
    data = {
        'injected_series': {
            col_name + "injected": {"linkedTo": col_name, "id": col_name + "injected", "name": col_name + "injected",
                                    "data": list(injected_data_container.injected[col_name])}
        } for (i, col_name) in enumerate(injected_data_container.truth.columns) if
        i in injected_data_container.injected_columns}
    return data


def get_repair_data(repair, injected_data_container, alg_name):
    truth = injected_data_container.truth
    repair.columns = truth.columns
    injected_data_container: InjectedDataContainer
    data = {
        col_name + "repair": {"linkedTo": col_name,
                              "id": col_name + "repair",
                              "name": alg_name,
                              "data": list(repair[col_name]),
                              "norm_data": list(repair[col_name])
                                  # list(repair[col_name])list((repair[col_name].values - np.mean(truth[col_name].values)) / np.std(
                                  # truth[col_name].values))
                              }
        for (i, col_name) in enumerate(injected_data_container.truth.columns) if
        i in injected_data_container.injected_columns}

    return data
