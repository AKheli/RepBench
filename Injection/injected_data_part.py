import numpy as np

from Injection.injection_checks import anomaly_check, anomaly_label_check, index_check
from Injection.label_generator import generate_column_labels, generate_df_labels
import hashlib
import pandas as pd


class InjectedDataContainer:
    def __init__(self, injected ,truth, *,class_df , labels , name):
        self.truth_ = truth  #contains the Original Series
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
        self.injected_columns = [i for i,v in enumerate(class_df.any(axis=0).values) if v]
        assert injected.shape == truth.shape
        self.check_original_rmse()


        self.check()

    def check(self):
        index_check(self.klass,self.injected,self.truth,self._labels_)
        anomaly_check(self.klass,self.injected,self.truth)
        anomaly_label_check(class_df=self.class_df,label_df=self._labels_)


    def __repr__(self):
        return f"{self.name}"

    @property
    def truth(self):
        return self.truth_.copy()


    @property
    def injected(self):
        return self.injected_.copy()

    @property
    def klass(self):
        return self.class_df.copy()

    @property
    def labels(self):
        self.check()
        return self._labels_.copy()

    @property
    def labels_rate(self):
        return self._labels_.iloc[:,self.injected_columns].mean().mean()

    @property
    def repair_inputs(self):
        self.check()
        return {"injected": self.injected,
                "truth": self.truth,
                "labels": self.labels,
                "columns_to_repair": self.injected_columns.copy(),
                }#"score_indices" : self.get_weights()}

    def add_repair(self, repair_results, repair_type, repair_name = None):
        self.check()
        repair_name = repair_type if repair_name is None else repair_name
        self.repair_names.append(repair_name)
        assert repair_name not in self.repairs , f" {repair_name} already in {self.repairs.keys()}"
        f"such a repair already exists:{repair_name}"

        repair = repair_results["repair"]
        assert repair.shape == self.labels.shape , (repair_name,repair.shape , self.labels.shape ,self.truth.shape, self.injected.shape)

        repair_dict = {
            "repair": repair_results["repair"],
            "name": repair_name,
            "type" : repair_type,
            "parameters" : repair_results["params"]
        }

        self.repairs[repair_name] = repair_dict

        repair_metrics = repair_results["scores"]
        repair_metrics["runtime"] = repair_results["runtime"]
        self.repair_metrics[(repair_name, repair_type)] = repair_metrics

    def check_original_rmse(self,check_labels = True):
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
        return result #str(hashlib.md5((str(self.truth)+str(self.injected)+str(self.labels)+str(additional_input)).encode()).hexdigest())


    @property
    def original_scores(self):
        from algorithms.estimator import Estimator
        return Estimator().scores(self.injected,self.truth,self.injected_columns,self.labels,predicted=self.injected)


    def randomize_labels(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.check()
        self.relabeled +=1
        self._labels_ = generate_df_labels(self.class_, seed=self.relabeled)
        self.check()

    