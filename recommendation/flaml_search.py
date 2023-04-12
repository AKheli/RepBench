import warnings
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from flaml import AutoML
from recommendation.utils import *
from recommendation.utils.file_parsers import store_estimator_results

def flaml_search(automl_settings,X_train,y_train,X_test=None,y_test=None ,*, file_suffix=None,verbose=-1,additional_info:dict=None):
    if additional_info is None:
        additional_info = {}

    automl = AutoML()

    automl_result_name = f"flaml_classifier_{automl_settings.get('metric')}_time_{automl_settings.get('time_budget')}"

    if file_suffix is not None:
        automl_result_name = f"{automl_result_name}_{file_suffix}"

    with  warnings.catch_warnings():
        warnings.simplefilter("ignore")
        automl.fit(X_train=X_train, y_train=y_train, verbose=verbose, **automl_settings)

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

    if X_test is None or y_test is None:
        results.update(additional_info)
        print(results)
        store_estimator_results(results, file_name=automl_result_name + "_results")
        return

    pred_y_test = (automl.model.estimator.predict(X_test))
    accuracy = np.mean(pred_y_test == y_test)
    conf_mat = confusion_matrix(y_test, pred_y_test, labels=np.unique(y_pred))
    class_report = classification_report(y_test, pred_y_test,  labels=np.unique(y_pred))

    # Store metrics in dictionary
    results["test"] = {
        'accuracy': accuracy,
        'confusion_matrix': conf_mat,
        'classification_report': class_report,
    }

    results.update(additional_info)
    store_estimator_results(results, file_name=automl_result_name + "_results")

