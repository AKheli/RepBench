import warnings
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from flaml import AutoML
from recommendation.utils import *
from recommendation.utils.file_parsers import store_estimator_results


def flaml_search(automl_settings, X_train, y_train, *, file_suffix=None, verbose=-1, ignore_flaml_output=True , file_name=None):
    automl = AutoML(**automl_settings)
    automl_result_name = f"flaml_classifier_{automl_settings.get('metric')}_time_{automl_settings.get('time_budget')}"

    if file_suffix is not None:
        automl_result_name = f"{automl_result_name}_{file_suffix}"

    if ignore_flaml_output:
        with  warnings.catch_warnings():
            warnings.simplefilter("ignore")
            automl.fit(X_train=X_train, y_train=y_train, verbose=verbose, **automl_settings)
    else:
        automl.fit(X_train=X_train, y_train=y_train, verbose=verbose, **automl_settings)

    store_estimator(automl, estimator_name=automl_result_name)
    return automl, automl_result_name


def compute_automl_scores(automl_or_automl_result_name, X_train, y_train, X_test, y_test, *, additional_info: dict = None
                          , plot_confusion_matrix=False,labels=None):
    if additional_info is None:
        additional_info = {}

    if isinstance(automl_or_automl_result_name, str):
        automl = load_estimator(automl_or_automl_result_name)
        automl_result_name = f"flaml_classifier_{automl._settings['metric']}_time_{automl._settings['time_budget']}"

    else:
        automl = automl_or_automl_result_name
        automl_result_name = f"flaml_classifier_{automl._settings['metric']}_time_{automl._settings['time_budget']}"

    assert isinstance(automl, AutoML)

    y_pred = (automl.model.estimator.predict(X_train))
    accuracy_train = np.mean(y_pred == y_train)
    conf_mat = confusion_matrix(y_train, y_pred)
    class_report = classification_report(y_train, y_pred)

    # Store metrics in dictionary
    results = {}
    results["train"] = {
        'accuracy': accuracy_train,
        'confusion_matrix': conf_mat,
        'classification_report': class_report,
    }

    if X_test is None or y_test is None:
        results.update(additional_info)
        print(results)
        store_estimator_results(results, file_name=automl_result_name + "_results")
        return

    pred_y_test = (automl.model.estimator.predict(X_test))
    accuracy_test = np.mean(pred_y_test == y_test)
    conf_mat = confusion_matrix(y_test, pred_y_test, labels=np.unique(y_pred))
    class_report = classification_report(y_test, pred_y_test, labels=np.unique(y_pred))

    # Store metrics in dictionary
    results["test"] = {
        'accuracy': accuracy_test,
        'confusion_matrix': conf_mat,
        'classification_report': class_report,
    }

    results.update(additional_info)

    store_estimator_results(results, file_name=automl_result_name + "_results")

    if plot_confusion_matrix:
        from sklearn.metrics import ConfusionMatrixDisplay
        disp = ConfusionMatrixDisplay(conf_mat,display_labels=labels)
        disp.plot()
        plt.show()

    print("train_accuracy", accuracy_train, "test_accuracy", accuracy_test , automl_result_name)
    return {"train_accuracy": accuracy_train, "test_accuracy": accuracy_test}
