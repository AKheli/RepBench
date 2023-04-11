import json

import numpy as np
import pandas as pd
import pickle


def parse_recommendation_results(file_name, error="rmse"):
    json_array = parse_lines_file(file_name)
    df_dict: dict = sub_results_from_json_array(json_array)
    if "alg_results" in df_dict:
        print(df_dict["alg_results"])
        df_dict["best_algorithm"] = df_dict["alg_results"].apply(lambda row: min_alg(row, error), axis=1)
        df_dict["best_algorithm_error"] = df_dict["alg_results"].apply(lambda row: min_error(row, error), axis=1)


    return df_dict


def min_alg(row, error):
    error_rows = row.apply(lambda r: r[error])
    return error_rows.idxmin()
def min_error(row, error):
    error_rows = row.apply(lambda r: r[error])
    return error_rows.min()

def parse_lines_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    json_string = "[" + ",".join(lines) + "]"
    json_array = json.loads(json_string)
    return json_array


def sub_results_from_json_array(json_array):
    # Create a dictionary of lists for each key
    result_dict = {}
    for item in json_array:
        for key, value in item.items():
            if isinstance(value, dict):
                if key in result_dict:
                    result_dict[key].append(value)
                else:
                    result_dict[key] = [value]
            else:
                if key in result_dict:
                    result_dict[key].append(value)
                else:
                    result_dict[key] = [value]

    # Create a DataFrame for each key
    result_frames = {}
    for key, values in result_dict.items():
        if isinstance(values[0], dict):
            result_frames[key] = pd.DataFrame.from_records(values)
        else:
            result_frames[key] = pd.DataFrame({key: values})

    return result_frames


def get_column_with_lowest_value(df):
    """Returns a new DataFrame with a single column containing the name of the column with the lowest value in each row"""
    return pd.DataFrame({'best_algorithm': df.idxmin(axis=1)})


def store_estimator(automl, estimator_name="bestEstimator"):
    with open(f'recommendation/automl_files/{estimator_name}.pkl', 'wb') as f:
        pickle.dump(automl, f, pickle.HIGHEST_PROTOCOL)


def load_estimator(estimator_name="bestEstimator"):
    """Loads a pickled automl resulst from the recommendation/automl_files directory
    Args:
        estimator_name (str): The name of the estimator to load
    Returns:
        automl (flaml.automl.AutoML): The loaded automl estimato

    usage example:
    automl.model.estimator.predict(X_test)
    """
    automl = pickle.load(open(f'recommendation/automl_files/{estimator_name}.pkl', 'rb'))
    return automl


json_numpy_encoder = lambda obj: obj.tolist() if isinstance(obj, np.ndarray) else obj


def store_estimator_results(results: dict, file_name: str):
    with open(f'recommendation/automl_files/{file_name}.json', 'w') as f:
        json.dump(results, f, indent=4, default=json_numpy_encoder)
