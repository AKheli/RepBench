import numpy as np
import pandas as pd
from pycatch22 import catch22_all
from tsfresh import extract_features as tsfresh_extract_features


def single_ts_feature_extraction(input_data):
    if isinstance(input_data, pd.Series):
        df_data = pd.DataFrame({'data': input_data.flatten()})
        np_data = df_data['data'].values
    else:
        assert isinstance(input_data, np.ndarray)
        np_data = input_data
        df_data = pd.DataFrame({'data': np_data.flatten()})

    catch22_features = catch22_all(np_data)
    catch22_features = {name: round(val, 4) for name, val in
                        zip(catch22_features["names"], catch22_features["values"])}

    df_data["id"] = [0 for _ in range(len(df_data))]
    tsfresh_features = tsfresh_extract_features(df_data, column_id="id")
    print(tsfresh_features)

    tsfresh_features = tsfresh_features[['data__skewness', 'data__kurtosis']]
    tsfresh_features = dict(zip(tsfresh_features.columns, tsfresh_features.values.flatten()))
    catch22_features.update(tsfresh_features)
    return catch22_features


def extract_features(dataset, column):
    single_features = single_ts_feature_extraction(dataset.iloc[:, column].values)
    return single_features
