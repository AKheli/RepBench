import json
import warnings
import pandas as pd
import sys
import os
import numpy as np
from flaml import AutoML
from recommendation.utils import *
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score

from recommendation.utils.file_parsers import store_estimator_results

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

feature_file_name = "recommendation/results/results_ucr_features"

# df = pd.read_json(feature_file_name)
# Initialize an AutoML instance
automl = AutoML()
# Specify automl goal and constraint

automl_settings = {
    "time_budget": 60*30,  # in seconds
    "metric": "macro_f1", # accuracy ,
    "task": 'classification',
    "log_file_name": "recommendation/logs/flaml.log",
}

automl_result_name = f"flaml_classifier_{automl_settings.get('metric')}_time_{automl_settings.get('time_budget')}"

algorithms_scores: pd.DataFrame
feature_values: pd.DataFrame
best_algorithms: pd.DataFrame
algorithms_scores, feature_values = parse_json_file(feature_file_name)
best_algorithms = get_column_with_lowest_value(algorithms_scores)

best_algorithms = best_algorithms.values.flatten()
encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

# Train with labeled input data
train_split_r = 0.8
train_split = int(len(feature_values) * train_split_r)

X_train = feature_values.iloc[:train_split, :]
X_test = feature_values.iloc[train_split:, :]

y_train, y_test = categories_encoded[:train_split], categories_encoded[train_split:]

with  warnings.catch_warnings():
    warnings.simplefilter("ignore")
    automl.fit(X_train=X_train, y_train=y_train, verbose=3, **automl_settings)

store_estimator(automl, estimator_name=automl_result_name)

y_pred = (automl.model.estimator.predict(X_train))
accuracy = np.mean(y_pred == y_train)
conf_mat = confusion_matrix(y_train, y_pred)
class_report = classification_report(y_train, y_pred)
# roc_auc = roc_auc_score(y_train, y_pred.reshape(-1, 1),multi_class='ovr')

# Store metrics in dictionary
results = {}
results["train"] = {
    'accuracy': accuracy,
    'confusion_matrix': conf_mat,
    'classification_report': class_report,
}

pred_y_test = (automl.model.estimator.predict(X_test))
accuracy = np.mean(pred_y_test == y_test)
conf_mat = confusion_matrix(y_test, pred_y_test)
class_report = classification_report(y_test, pred_y_test)
# roc_auc = roc_auc_score(y_test, y_pred.reshape(-1, 1),multi_class='ovr')

# Store metrics in dictionary
results["test"] = {
    'accuracy': accuracy,
    'confusion_matrix': conf_mat,
    'classification_report': class_report,
}

store_estimator_results(results, file_name=automl_result_name + "_results")
