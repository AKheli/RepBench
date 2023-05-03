import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from injection.injected_data_container import InjectedDataContainer
from injection.label_generator import generate_df_labels


def create_injected_container(* , injected_df, truth_df,container_does_rmse_checks=True):
    assert injected_df.index.equals(truth_df.index), f"{injected_df.index},{truth_df.index}"
    assert injected_df.shape == truth_df.shape, f"{injected_df},{truth_df}"

    # plt.plot(injected_df.iloc[:,:3])
    # plt.title("loaded injected")
    # plt.show()

    class_df = pd.DataFrame(np.invert(np.isclose(truth_df.values, injected_df.values))
                            , index=injected_df.index, columns=injected_df.columns)

    assert class_df.isnull().sum().sum() == 0, (truth_df,)

    label_df: pd.DataFrame = generate_df_labels(class_df)


    assert class_df.index.equals(truth_df.index)
    assert label_df.index.equals(truth_df.index)

    assert injected_df.shape == truth_df.shape
    injected_container = InjectedDataContainer(injected_df, truth_df, class_df=class_df,
                                                name="repair_df",
                                                labels=label_df,check_rmse=container_does_rmse_checks)

    # plt.plot(injected_df.iloc[:,:3])
    # plt.title("loaded injected")
    # plt.show()


    return injected_container



def injected_container_None_Series( truth_df , injected_series_dicts):
    print("truth_df" , truth_df)
    print(injected_series_dicts)
    injected_df = truth_df.copy()
    for series_dict in injected_series_dicts:
        col_name, data = series_dict["linkedTo"] ,  series_dict["data"]
        injected_data= np.array(data,dtype=float)
        values_to_repalce = ~np.isnan(injected_data)
        injected_df.loc[values_to_repalce,col_name] = injected_data[values_to_repalce]

    injected_data_container = create_injected_container(injected_df=injected_df,truth_df=truth_df)
    return injected_data_container



