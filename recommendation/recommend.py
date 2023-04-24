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
autoML_file_name_default = "flaml_classifier_accuracy_time_600_non_normalized"


def get_recommendation(injected_data_container: InjectedDataContainer,
                       autoML_file_name: str = autoML_file_name_default) -> dict:
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

    automl: AutoML = load_estimator(autoML_file_name)
    features = extract_features(injected_data_container.injected, injected_data_container.injected_columns[0])
    fd = pd.DataFrame.from_dict({k: [v] for k, v in features.items()})

    best_algorithm = automl.predict(fd)[0]
    label_inverse = automl._label_transformer.inverse_transform

    probabilities = {label_inverse([i])[0]: p for i, p in enumerate(automl.predict_proba(fd)[0])}
    used_estimator = automl.best_estimator
    results = {
        "recommended_algorithm": best_algorithm,
        "probabilities": probabilities,
        "alg_repairs": alg_repairs,
        "alg_score": alg_scores,
        "alg_parameters": alg_parameters,
        "used_estimator": used_estimator,
        "data_features": features
    }
    return results


def get_recommendation_non_containerized(anomalous_ts, *,column_for_recommendation , label_df=None,
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
        if not ( label_df is None and alg_name == IMR):
            alg_constructor = algo_mapper[alg_name]
            parameters = get_algorithm_params(alg_name)
            alg_repair = alg_constructor(**parameters).repair(anomalous_ts,truth=None,columns_to_repair=[column_for_recommendation], labels=label_df)
            alg_repairs[alg_name] = alg_repair

    if label_df is None:
        #filter out IMR
        p_imr = probabilities.pop(IMR)
        resulting_probability = 1- p_imr
        probabilities = {k: v / resulting_probability for k, v in probabilities.items()}
        best_algorithm = max(probabilities, key=probabilities.get)
        results["recommended_algorithm"] = best_algorithm
        results["probabilities"] = probabilities

    results["alg_repairs"] = alg_repairs

    return results
