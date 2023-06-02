def get_relevant_parameters(config):
    """ extra parameters from a config
        for the parameter values see:
        https://microsoft.github.io/FLAML/docs/Use-Cases/Task-Oriented-AutoML/
    """
    model = config.get("model", None) or config.get("estimator", None)
    assert model is not None, "model or estimator must be specified in config"

    parameters = {}
    try:
        if model == "RandomForest":
            parameters["n_estimators"] = config["n_estimators"]
            parameters["max_features"] = round(config["max_features"],4)
            parameters["max_leaf_nodes"] = config["max_leaf_nodes"]

        elif model == "ExtraTrees":
            parameters["n_estimators"] = config["n_estimators"]
            parameters["max_features"] = round(config["max_features"],4)
            parameters["max_leaf_nodes"] = config["max_leaf_nodes"]

        elif model == "LogisticRegression":
            parameters["C"] = round(config["C"],4)

        elif model == "LGBM":
            parameters["n_estimators"] = config["n_estimators"]
            parameters["num_leaves"] = config["num_leaves"]
            parameters["learning_rate"] = round(config["learning_rate"], 4)
            parameters["min_child_samples"] = config["min_child_samples"]

        elif model == "XGBoostSklearn":
            parameters["n_estimators"] = config["n_estimators"]
            parameters["max_depth"] = config["max_depth"]
            parameters["learning_rate"] = round(config["learning_rate"], 4)
            parameters["min_child_weight"] = round(config["min_child_weight"],4)
            parameters["reg_alpha"] = round(config["reg_alpha"],4)
            parameters["reg_lambda"] = round(config["reg_lambda"],4)

        else:
            assert False, f"model {model} not Found"
    except KeyError as e:
        raise KeyError(f"Parameter {e} not found in config {config}")

    return parameters


parameters_dict = {
    "RandomForest": ["n_estimators", "max_features", "max_leaf_nodes"],
    "ExtraTrees": ["n_estimators", "max_features", "max_leaf_nodes"],
    "LogisticRegression": ["C"],
    "LGBM": ["n_estimators", "num_leaves", "learning_rate", "min_child_samples"],
    "XGBoostSklearn": ["n_estimators", "max_depth", "learning_rate", "min_child_weight", "reg_alpha", "reg_lambda"]
}
