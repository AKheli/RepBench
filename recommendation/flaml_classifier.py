import json
import pandas as pd
import sys
import os
from flaml import AutoML
from recommendation.utils import parse_json_file , get_column_with_lowest_value

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

feature_file_name = "recommendation/results/results_features"

# df = pd.read_json(feature_file_name)
# Initialize an AutoML instance
automl = AutoML()
# Specify automl goal and constraint
automl_settings = {
    "time_budget": 100,  # in seconds
    "metric": 'F1',
    "task": 'classification',
    "log_file_name": "recommendation/logs/flaml.log",
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
