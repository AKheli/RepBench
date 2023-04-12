import numpy as np
import pandas as pd
from pycatch22 import catch22_all
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters
from tsfresh import extract_features as tsfresh_extract_features


def single_ts_feature_extraction(input_data):
    if isinstance(input_data, pd.Series):
        df_data = pd.DataFrame({'data': input_data.flatten()})
        np_data = df_data['data'].values
    else:
        assert isinstance(input_data, np.ndarray)
        np_data = input_data
        df_data = pd.DataFrame({'data': np_data.flatten()})

    features = {}
    catch22_features = extract_catch22_features(np_data)

    tsfresh_features_minimal = extract_ts_fresh_features(np_data)
    # tsfresh_features_efficient = extract_ts_fresh_features(np_data, FCParameters=EfficientFCParameters())

    features.update(catch22_features)
    # features.update(tsfresh_features_efficient)
    features.update(tsfresh_features_minimal)
    return features


def multi_ts_feature_extraction(dataset: pd.DataFrame, column):
    n, m = dataset.shape

    corr: np.array = dataset.corr().values
    col_corr = corr[:, column]
    col_corr__mean, col_corr_median = np.mean(col_corr), np.median(col_corr)
    col_corr_abs_mean, col_corr_abs_median = np.mean(np.abs(col_corr)), np.median(np.abs(col_corr))

    corr_abs_mean, corr_abs_median = np.mean(np.abs(corr)), np.median(np.abs(corr))
    n_ts = m

    multi_dim_features = {
        "col_corr__mean": col_corr__mean,
        "col_corr_median": col_corr_median,
        "col_corr_abs_mean": col_corr_abs_mean,
        "col_corr_abs_median": col_corr_abs_median,
        "corr_abs_mean": corr_abs_mean,
        "corr_abs_median": corr_abs_median,
        "n_ts": n_ts
    }
    return multi_dim_features


def extract_features(dataset, column):  # for one columns only
    single_features = single_ts_feature_extraction(dataset.iloc[:, column].values)
    multi_features = multi_ts_feature_extraction(dataset, column)
    single_features.update(multi_features)
    return single_features


def extract_catch22_features(data: np.ndarray):
    catch22_features = catch22_all(data)
    catch22_features = {name: round(val, 4) for name, val in
                        zip(catch22_features["names"], catch22_features["values"])}

    return catch22_features


def extract_ts_fresh_features(data: np.ndarray, FCParameters=MinimalFCParameters()):
    df_data = pd.DataFrame({'data': data.flatten()})
    df_data["id"] = [0 for _ in range(len(df_data))]
    df_data["time"] = list(range(len(df_data)))
    tsfresh_features = tsfresh_extract_features(df_data, column_id="id", column_sort="time",
                                                default_fc_parameters=FCParameters,
                                                show_warnings=False,
                                                disable_progressbar=True)
    tsfresh_features = dict(zip(tsfresh_features.columns, tsfresh_features.values.flatten()))
    return tsfresh_features


def subset_features(feature_df: pd.DataFrame, feature_names: list):
    return feature_df[feature_names]


def get_tsfresh__minimal_names(FCParameters):
    return ["data__" + s for s in list(FCParameters)]


features_values = {"catch22": catch22_all([0, 0, 0, 0, 0, 1])["names"],
                   "tsfresh_minimal": get_tsfresh__minimal_names(MinimalFCParameters()),
                   "tsfresh_efficient": EfficientFCParameters(),  # not added yet
                   "multi_dim": ["col_corr__mean", "col_corr_median", "col_corr_abs_mean", "col_corr_abs_median"
                       , "corr_abs_mean", "corr_abs_median", "n_ts"]
                   }
