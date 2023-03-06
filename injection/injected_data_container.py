import numpy as np

from injection.injection_checks import anomaly_check, anomaly_label_check, index_check
from injection.label_generator import  generate_df_labels
import hashlib
import pandas as pd


class InjectedDataContainer:
    def __init__(self, injected, truth, *, class_df, labels, name):
        self.truth_ = truth  # contains the Original Series
        self.injected_ = injected
        self._labels_ = labels
        self.repairs = {}
        self.repair_metrics = {}
        self.repair_names = []
        self.name = name
        self.relabeled = 0

        if class_df is None:
            class_df = pd.DataFrame(np.invert(np.isclose(injected, truth))).reindex_like(truth)
        self.class_df = class_df
        self.injected_columns = [i for i, v in enumerate(class_df.any(axis=0).values) if v]
        assert injected.shape == truth.shape
        self.check_original_rmse()

        self.check()

    def check(self):
        index_check(self.klass, self.injected, self.truth, self._labels_)
        anomaly_check(self.klass, self.injected, self.truth)
        anomaly_label_check(class_df=self.class_df, label_df=self._labels_)

    def __repr__(self):
        return f"{self.name}"

    @property
    def truth(self):
        return self.truth_.copy()

    @property
    def injected(self):
        return self.injected_.copy()

    def get_none_filled_injected(self):
        injected = self.injected.copy()
        for col in self.injected.columns:
            # convolve over class df setting each entry next to a true entry to true
            class_col = self.class_df[col].values
            class_col = np.convolve(class_col, [1, 1, 1], mode="same") > 0
            injected.loc[~class_col, col] = np.nan
        return injected

    def get_anomaly_info(self):
        import functools
        #get number of preceding 1 per col
        for col in self.class_df:
            last = False
            class_col = self.class_df[col].values
            for v in class_col:

                last = v




    @property
    def klass(self):
        return self.class_df.copy()

    @property
    def labels(self):
        self.check()
        return self._labels_.copy()

    @property
    def labels_rate(self):
        return self._labels_.iloc[:, self.injected_columns].mean().mean()

    @property
    def repair_inputs(self):
        self.check()
        return {"injected": self.injected,
                "truth": self.truth,
                "labels": self.labels,
                "columns_to_repair": self.injected_columns.copy(),
                }

    @property
    def a_perc(self):
        return np.mean(self.klass.iloc[:, self.injected_columns].values)

    def add_repair(self, repair_results, repair_type, repair_name=None):
        self.check()
        repair_name = repair_type if repair_name is None else repair_name
        self.repair_names.append(repair_name)
        assert repair_name not in self.repairs, f" {repair_name} already in {self.repairs.keys()}"
        f"such a repair already exists:{repair_name}"

        repair = repair_results["repair"]
        assert repair.shape == self.labels.shape, (
        repair_name, repair.shape, self.labels.shape, self.truth.shape, self.injected.shape)

        repair_dict = {
            "repair": repair_results["repair"],
            "name": repair_name,
            "type": repair_type,
            "parameters": repair_results["params"]
        }

        self.repairs[repair_name] = repair_dict

        repair_metrics = repair_results["scores"]
        repair_metrics["runtime"] = repair_results["runtime"]
        self.repair_metrics[(repair_name, repair_type)] = repair_metrics

    def check_original_rmse(self, check_labels=True):
        assert np.any(self.klass.values)
        weights = np.zeros_like(self.injected.values)
        weights[self.klass] = 1
        if check_labels:
            weights[self.labels] = 0
        weights = weights.flatten()
        assert np.any(weights)

    def hash(self, additional_input=""):
        m = hashlib.md5(self.injected.values.flatten())
        m.update(self.labels.values.flatten())
        m.update(additional_input.encode())
        result = m.hexdigest()
        return result

    @property
    def original_scores(self):
        from algorithms.estimator import Estimator
        return Estimator().scores(self.injected, self.truth, self.injected_columns, self.labels,
                                  predicted=self.injected)


    def get_a_rate_per_col(self,rounding=3):
        result = {}
        cols = self.injected.columns
        for col in cols:
            result[col] = round(np.mean(self.class_df[col].values),rounding)
        return result

    def get_truth_correlation(self):
        return self.truth.corr()

    def get_injected_correlation(self):
        return self.injected.corr()

    def randomize_labels(self):
        self.check()
        self.relabeled += 1
        self._labels_ = generate_df_labels(self.class_, seed=self.relabeled)
        self.check()


    def set_to_original_scale(self, mean, std):
        self.injected_ = self.injected_ * std + mean
        self.truth_ = self.truth_ * std + mean
        close = np.isclose(self.truth.values, self.injected.values)
        assert np.allclose(~close, self.class_df.values)

    # dump to json
    def to_json(self):
        import json
        result = {
            "name": self.name,
            "truth": self.truth.to_json(),
            "injected": self.injected.to_json(),
            "labels": self.labels.to_json(),
            "class_df": self.class_df.to_json(),
            "repairs": {k: v.to_json() for k, v in self.repairs.items()},
            "repair_metrics": self.repair_metrics,
            "repair_names": self.repair_names,
        }
        return json.dumps(result)

    @staticmethod
    def from_json(json_string):
        import json
        result = json.loads(json_string)
        return InjectedDataContainer(
            injected=pd.read_json(result["injected"]),
            truth=pd.read_json(result["truth"]),
            labels=pd.read_json(result["labels"]),
            class_df=pd.read_json(result["class_df"]),
            name=result["name"],
        )

    def save(self, folder="data"):
        import os
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.truth.to_csv(f"{folder}/{self.name}_truth.csv")
        self.injected.to_csv(f"{folder}/{self.name}_injected.csv")
        self.labels.to_csv(f"{folder}/{self.name}_labels.csv")
        self.class_df.to_csv(f"{folder}/{self.name}_class_df.csv")
        # dict to csv
        import csv
        with open(f"{folder}/{self.name}_repairs.csv", 'w') as f:
            w = csv.writer(f)
            w.writerows(self.repairs.items())


