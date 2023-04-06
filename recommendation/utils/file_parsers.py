import json

import numpy as np
import pandas as pd
import pickle


def parse_json_file(file_name):
    """
    Parses a JSON file with algorithm results and feature data, and returns two pandas DataFrames:
    one containing the algorithm RMSE values, and one containing the feature values.

    Args:
        file_name (str): The name of the JSON file to parse.

    Returns:
        algorithm_df (pandas.DataFrame): A DataFrame with algorithm RMSE values, where each column
            corresponds to an algorithm name and each row corresponds to a set of feature values.
        feature_df (pandas.DataFrame): A DataFrame with feature values, where each column corresponds
            to a feature name and each row corresponds to a set of algorithm RMSE values.
    """
    with open(file_name, 'r') as f:
        algorithm_data = {}
        feature_data = {}
        for line in f:
            json_data = json.loads(line.strip())
            for algorithm, algorithm_results in json_data['alg_results'].items():
                if algorithm not in algorithm_data:
                    algorithm_data[algorithm] = []
                algorithm_data[algorithm].append(algorithm_results['rmse'])
            for feature, feature_value in json_data['features'].items():
                if feature not in feature_data:
                    feature_data[feature] = []
                feature_data[feature].append(feature_value)
        algorithm_df = pd.DataFrame(algorithm_data)
        feature_df = pd.DataFrame(feature_data)
    return algorithm_df, feature_df



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

def store_estimator_results(results : dict ,file_name: str):
    with open(f'recommendation/automl_files/{file_name}.json', 'w') as f:
       json.dump(results, f, indent=4, default=json_numpy_encoder)
