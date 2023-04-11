import warnings
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

feature_file_name = "recommendation/results/results_without_cd_features"

# df = pd.read_json(feature_file_name)
# Initialize an AutoML instance
automl = AutoML()
# Specify automl goal and constraint

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']


# algorithms_scores: pd.DataFrame
# feature_values: pd.DataFrame
# best_algorithms: pd.DataFrame
algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

# Train with labeled input data
## Split data into train and test sets

train_split_r = 0.8
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)
#get all other indices
test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)

X_train = feature_values.iloc[train_split, :]
X_test = feature_values.iloc[test_split, :]

y_train, y_test = categories_encoded[train_split], categories_encoded[test_split]


for metric in multiclass_metrics:
    for time_budget in [60,  180, 60*20,60*60]:
        automl_settings = {
            "time_budget": time_budget,  # in seconds
            "metric": metric, # accuracy , micro_f1, macro_f1
            "task": 'classification',
            "log_file_name": "recommendation/logs/flaml.log",
        }

        automl_result_name = f"flaml_classifier_{automl_settings.get('metric')}_time_{automl_settings.get('time_budget')}"

        with  warnings.catch_warnings():
            warnings.simplefilter("ignore")
            automl.fit(X_train=X_train, y_train=y_train, verbose=3, **automl_settings)

        store_estimator(automl, estimator_name=automl_result_name)

        y_pred = (automl.model.estimator.predict(X_train))
        label_names = encoder.inverse_transform(np.unique(y_pred))
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
        conf_mat = confusion_matrix(y_test, pred_y_test, labels = np.unique(y_pred))
        class_report = classification_report(y_test, pred_y_test , target_names=label_names,labels = np.unique(y_pred) )
        # roc_auc = roc_auc_score(y_test, y_pred.reshape(-1, 1),multi_class='ovr')

        # Store metrics in dictionary
        results["test"] = {
            'accuracy': accuracy,
            'confusion_matrix': conf_mat,
            'classification_report': class_report,
        }

        store_estimator_results(results, file_name=automl_result_name + "_results")
