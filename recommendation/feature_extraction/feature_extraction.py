import numpy as np
import pandas as pd
from pycatch22 import catch22_all
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters
from tsfresh import extract_features as tsfresh_extract_features

from recommendation.feature_extraction.ts_fresh_features import selected_feature_names


feature_endings = {"catch22": "__ct",
                   "tsfresh_minimal": "__tsf_m",
                   "multi_dim": "__md",
                   "tsfresh_selected": "__tsf_s"
                   }

def single_ts_feature_extraction(input_data):
    if isinstance(input_data, pd.Series):
        df_data = pd.DataFrame({'data': input_data.flatten()})
        np_data = df_data['data'].values
    else:
        assert isinstance(input_data, np.ndarray)
        np_data = input_data
        df_data = pd.DataFrame({'data': np_data.flatten()})

    features = {}
    selected_tsfresh_features = extract_selected_ts_fresh_features(np_data)
    catch22_features = extract_catch22_features(np_data)
    tsfresh_features_minimal = extract_ts_fresh_features(np_data)

    features.update(catch22_features)
    features.update(selected_tsfresh_features)
    features.update(tsfresh_features_minimal)
    return features


def multi_ts_feature_extraction(dataset: pd.DataFrame, column):
    n, m = dataset.shape

    corr: np.array = dataset.corr().values

    assert np.isnan(corr).sum() == 0, dataset

    col_corr = corr[:, column]
    col_corr__mean, col_corr_median = np.mean(col_corr), np.median(col_corr)
    col_corr_abs_mean, col_corr_abs_median = np.mean(np.abs(col_corr)), np.median(np.abs(col_corr))

    corr_abs_mean, corr_abs_median = np.mean(np.abs(corr)), np.median(np.abs(corr))
    n_ts = m

    # no nan values
    assert not np.isnan(col_corr__mean), corr
    assert not np.isnan(col_corr_median), corr
    assert not np.isnan(col_corr_abs_mean), corr
    assert not np.isnan(col_corr_abs_median), corr
    assert not np.isnan(corr_abs_mean), corr
    assert not np.isnan(corr_abs_median), corr

    multi_dim_features = {
        "col_corr__mean": col_corr__mean,
        "col_corr_median" : col_corr_median,
        "col_corr_abs_mean" : col_corr_abs_mean,
        "col_corr_abs_median": col_corr_abs_median,
        "corr_abs_mean" : corr_abs_mean,
        "corr_abs_median": corr_abs_median,
        "n_ts" : n_ts
    }
    multi_dim_features = {name + feature_endings["multi_dim"]:val for name, val in multi_dim_features.items()}
    return multi_dim_features


def extract_features(dataset, column):  # for one columns only
    single_features = single_ts_feature_extraction(dataset.iloc[:, column].values)
    multi_features = multi_ts_feature_extraction(dataset, column)
    single_features.update(multi_features)
    return single_features


def extract_catch22_features(data: np.ndarray):
    catch22_features = catch22_all(data)
    catch22_features = {name + feature_endings["catch22"]: round(val, 4) for name, val in
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

    tsfresh_features_name = [s.replace('"', '').replace("data__", "") + feature_endings["tsfresh_minimal"] for s in tsfresh_features.columns]
    tsfresh_features = dict(zip(tsfresh_features_name, tsfresh_features.values.flatten()))
    return tsfresh_features


def extract_selected_ts_fresh_features(data: np.ndarray):
    from recommendation.feature_extraction.ts_fresh_features import selected_ts_fresh_features

    df_data = pd.DataFrame({'data': data.flatten()})
    df_data["id"] = [0 for _ in range(len(df_data))]
    df_data["time"] = list(range(len(df_data)))
    tsfresh_features = tsfresh_extract_features(df_data, column_id="id", column_sort="time",
                                                default_fc_parameters=selected_ts_fresh_features)

    tsfresh_features_name = [s.replace('"', '').replace("data__", "") + feature_endings["tsfresh_selected"] for s in
                             tsfresh_features.columns]
    tsfresh_features = dict(zip(tsfresh_features_name, tsfresh_features.values.flatten()))

    return tsfresh_features






