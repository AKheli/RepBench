import json
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

feature_file_name = "recommendation/results/results_features"

def parse_json_file(file_name):
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



print(parse_json_file(feature_file_name)[0])
print(parse_json_file(feature_file_name)[1])
print(get_column_with_lowest_value(parse_json_file(feature_file_name)[0]))
# df = pd.read_json(feature_file_name)
from flaml import AutoML

# Initialize an AutoML instance
automl = AutoML()
# Specify automl goal and constraint
automl_settings = {
    "time_budget": 100,  # in seconds
    "metric": 'accuracy',
    "task": 'classification',
    "log_file_name": "flaml.log",
}

algorithms_scores :  pd.DataFrame
feature_values : pd.DataFrame
best_algorithms : pd.DataFrame
algorithms_scores , feature_values = parse_json_file(feature_file_name)
best_algorithms = get_column_with_lowest_value(algorithms_scores)

# Train with labeled input data
automl.fit(X_train=feature_values, y_train=best_algorithms.values)
# Predict
print(feature_values)
print(automl.predict_proba(feature_values))
# Print the best model
print(automl.model.estimator)
