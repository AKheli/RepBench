from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score , f1_score
from ray import tune




def run_ray_tune(config,X,y):
    time_budget = config.pop("time_budget",20)
    def train_model(config):
        if config["estimator"] == "RandomForest":
            model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                           max_depth=config["max_depth"],
                                           min_samples_split=config["min_samples_split"])
        elif config["estimator"] == "LGBM":
            model = LGBMClassifier(n_estimators=config["n_estimators"],
                                   num_leaves=config["num_leaves"],
                                   learning_rate=config["learning_rate"],
                                   min_child_samples=config["min_child_samples"])
        elif config["estimator"] == "ExtraTrees":
            model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
                                         max_depth=config["max_depth"],
                                         min_samples_split=config["min_samples_split"])
        elif config["estimator"] == "LogisticRegression":
            model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')

        model.fit(X, y)
        accuracy = accuracy_score(y, model.predict(X))
        tune.report(accuracy=accuracy, f1_score=f1_score(y, model.predict(X), average='micro'))

    return tune.run(train_model, config=config, time_budget_s=20 ,num_samples=1000)  ## analysis
