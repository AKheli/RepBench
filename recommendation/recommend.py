from flaml import AutoML
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/reccomendation.py

from algorithms import algo_mapper
from algorithms.param_loader import get_algorithm_params
from injection.injected_data_container import InjectedDataContainer

from algorithms.algorithms_config import CDREC, RPCA, IMR, SCREEN
from recommendation.feature_extraction.feature_extraction import extract_features
from recommendation.utils.file_parsers import load_estimator
from injection import get_injected_container_example

alg_names = [CDREC, RPCA, IMR, SCREEN]
# injected_data_container: InjectedDataContainer = get_injected_container_example()
autoML_file_name_default = "flaml_classifier_accuracy_time_6_non_normalized"


def get_recommendation(injected_data_container: InjectedDataContainer, classifier):
    features = extract_features(injected_data_container.injected, injected_data_container.injected_columns[0])
    print("FEATURES",features.keys())
    used_features = classifier.feature_names_in_
    print("Modelfeatures", list(used_features))

    fd = pd.DataFrame.from_dict({f_name: [v] for f_name, v in features.items() if f_name in used_features })
    print("final features" , fd.columns)


    probabilities = classifier.predict_proba(fd).flatten()
    recommended_algorithm = classifier.predict(fd).flatten()

    from recommendation.encoder import decode
    recommended_algorithm = decode(recommended_algorithm)
    labels = classifier.classes_
    probabilities = {decode(label): p for label, p in zip(labels, probabilities)}

    results = {
        "best_estimator" : recommended_algorithm,
        "recommended_algorithm": recommended_algorithm,
        "probabilities": probabilities,
        "used_estimator": str(classifier.__class__.__name__.split("Estimator")[0]),
        "data_features": features
    }
    print(results)


def get_all_repairs(injected_data_container: InjectedDataContainer):
    alg_scores = {}
    alg_parameters = {}
    alg_repairs = {}
    for alg_name in alg_names:
        alg_constructor = algo_mapper[alg_name]
        parameters = get_algorithm_params(alg_name)
        alg_repair = alg_constructor(**parameters).repair(**injected_data_container.repair_inputs)
        alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs, predicted=alg_repair)
        alg_score.pop("rmse_per_col", None)
        alg_score.pop("original_RMSE", None)

        alg_parameters[alg_name] = parameters
        alg_scores[alg_name] = alg_score
        alg_repairs[alg_name] = alg_repair

    result = {
        "alg_repairs": alg_repairs,
        "alg_scores": alg_scores,
        "alg_parameters": alg_parameters,
    }
    print(result)
    return result


def get_recommendation_and_repair(injected_data_container: InjectedDataContainer, classifier):
    results : dict = get_recommendation(injected_data_container, classifier)
    results.update(get_all_repairs(InjectedDataContainer))
    return results


def get_recommendation(injected_data_container: InjectedDataContainer, *,
                       autoML_file_name: str = autoML_file_name_default, automl: AutoML = None) -> dict:
    """
    Returns dict: {
    "recommended_algorithm" : str
    "probabilities" : dict : alg -> float
    "alg_repairs" : dict : alg -> array
    alg_score :    dict  : alg -> errors
    alg_parameters : alg -> param_dict
    "used_classifier" : str e.g lgbm
    "injected_ts" : col_n
    "data_features" : dict "feature_name" -> val
    }
    """

    print("get recommendation")
    alg_scores = {}
    alg_parameters = {}
    alg_repairs = {}
    for alg_name in alg_names:
        alg_constructor = algo_mapper[alg_name]
        parameters = get_algorithm_params(alg_name)
        alg_repair = alg_constructor(**parameters).repair(**injected_data_container.repair_inputs)
        alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs, predicted=alg_repair)
        alg_score.pop("rmse_per_col", None)
        alg_score.pop("original_RMSE", None)

        alg_parameters[alg_name] = parameters
        alg_scores[alg_name] = alg_score
        alg_repairs[alg_name] = alg_repair

    automl: AutoML = load_estimator(autoML_file_name) if automl is None else automl
    features = extract_features(injected_data_container.injected, injected_data_container.injected_columns[0])

    try:
        used_features = automl.feature_names_in_
    except:
        used_features = automl.feature_name_ ##some classifiers have feature_name_ instead of features_names_in_
    print("used features",used_features)

    print("Modelfeatures", list(used_features))

    fd = pd.DataFrame.from_dict({f_name: [v] for f_name, v in features.items() if f_name in used_features})

    from recommendation.encoder import decode

    predictions = automl.predict(fd)
    best_algorithm = decode(predictions)
    probabilities = {str(decode(i)): p for i, p in enumerate(automl.predict_proba(fd)[0])}
    try:
        used_estimator = automl.best_estimator
    except:
        used_estimator= str(automl.__class__.__name__.split("Estimator")[0])

    results = {
        "recommended_algorithm": best_algorithm,
        "probabilities": probabilities,
        "alg_repairs": alg_repairs,
        "alg_scores": alg_scores,
        "alg_parameters": alg_parameters,
        "used_estimator": used_estimator,
        "data_features": features
    }

    return results


def get_recommendation_non_containerized(anomalous_ts, *, column_for_recommendation, label_df=None,
                                         truth=None, autoML_file_name: str = autoML_file_name_default) -> dict:
    automl: AutoML = load_estimator(autoML_file_name)
    features = extract_features(anomalous_ts, column_for_recommendation)
    fd = pd.DataFrame.from_dict({k: [v] for k, v in features.items()})

    best_algorithm = automl.predict(fd)[0]
    label_inverse = automl._label_transformer.inverse_transform

    probabilities = {label_inverse([i])[0]: p for i, p in enumerate(automl.predict_proba(fd)[0])}
    used_estimator = automl.best_estimator
    results = {
        "recommended_algorithm": best_algorithm,
        "probabilities": probabilities,
        "used_estimator": used_estimator,
        "data_features": features
    }

    alg_repairs = {}
    for alg_name in alg_names:
        if not (label_df is None and alg_name == IMR):
            alg_constructor = algo_mapper[alg_name]
            parameters = get_algorithm_params(alg_name)
            alg_repair = alg_constructor(**parameters).repair(anomalous_ts, truth=None,
                                                              columns_to_repair=[column_for_recommendation],
                                                              labels=label_df)
            alg_repairs[alg_name] = alg_repair

    if label_df is None:
        # filter out IMR
        p_imr = probabilities.pop(IMR)
        resulting_probability = 1 - p_imr
        probabilities = {k: v / resulting_probability for k, v in probabilities.items()}
        best_algorithm = max(probabilities, key=probabilities.get)
        results["recommended_algorithm"] = best_algorithm
        results["probabilities"] = probabilities

    results["alg_repairs"] = alg_repairs

    return results
