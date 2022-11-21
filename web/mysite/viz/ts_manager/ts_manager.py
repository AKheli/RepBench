import pandas as pd
from pandas import DataFrame

from Injection.injected_data_part import InjectedDataContainer


def load_data_set(setname, type="train"):
    df: DataFrame = pd.read_csv(f"data/{type}/{setname}.csv")
    return df






## mapping to highcharts series
def get_truth_data(setname="bafu5k", viz=5, type="train"):
    df = load_data_set(setname, type=type)

    data = {
        'series': [{"visible": i < viz, "id": col_name, "name": col_name, "data": list(df[col_name])} for (i, col_name)
                   in
                   enumerate(df.columns)],
    }
    return data

def get_injected_data(injected_data_container):
    injected_data_container: InjectedDataContainer
    data = {
        'injected_series': {
            col_name + "injected": {"linkedTo": col_name, "id": col_name + "injected", "name": col_name + "injected",
                                    "data": list(injected_data_container.injected[col_name])}
        } for (i, col_name) in enumerate(injected_data_container.truth.columns) if i in injected_data_container.injected_columns}
    return data


def get_repair_data(repair,injected_data_container,alg_name):
    repair.columns = injected_data_container.truth.columns
    injected_data_container: InjectedDataContainer
    data ={
            col_name + "repair": {"linkedTo": col_name, "id": col_name + "repair", "name": alg_name,
                                    "data": list(repair[col_name])}
         for (i, col_name) in enumerate(injected_data_container.truth.columns) if i in injected_data_container.injected_columns}
    return data
