import numpy as np
import sklearn.metrics as sm

import hashlib

class DataPart:
    def __init__(self, injected, truth, class_,labels , train, name , a_type ):
        self.injected_ = injected
        self.truth_ = truth
        self.class_ = class_

        injected_bool = self.class_.any()
        self.injected_columns = np.arange(len(injected_bool))[injected_bool]
        self.train_: DataPart = train
        self.labels_ = labels

        if train is not None:
            assert train.train is None

        self.repairs = {}
        self.repair_metrics = {}
        self.repair_names = []
        self.check_original_rmse()

        self.a_type = a_type
        self.name = name


    def __repr__(self):
        return f"{self.name}_{self.a_type}"

    @property
    def truth(self):
        return self.truth_

    @property
    def train(self):
        assert isinstance(self.train_, DataPart) or self.train_ is None
        return self.train_

    @property
    def injected(self):
        return self.injected_.copy()

    @property
    def klass(self):
        return self.class_

    @property
    def labels(self):
        return self.labels_



    @staticmethod
    def get_anomaly_ranges(ts_class):
        in_anomaly = False
        ranges = []
        current_range = []
        for i, v in enumerate(ts_class):
            if v:
                in_anomaly = True
                current_range.append(i)
            if not v:
                if in_anomaly:
                    in_anomaly = False
                    ranges.append(current_range)
                    current_range = []
        return [np.array(range_) for range_ in ranges]

    @property
    def repair_inputs(self):
        return {"injected": self.injected,
                "truth": self.truth,
                "labels": self.labels,
                "columns_to_repair": self.injected_columns,
                }#"score_indices" : self.get_weights()}

    def add_repair(self, repair_results, repair_type, repair_name = None):
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

    def check_original_rmse(self):
        assert np.any(self.class_.values)
        weights = np.zeros_like(self.injected.values)
        weights[self.class_] = 1
        weights[self.labels] = 0
        weights = weights.flatten()

        assert np.any(weights)
        injected_np = self.injected.values.flatten()
        truth_np = self.truth.values.flatten()


    def hash(self, additional_input=""):
        m = hashlib.md5(self.injected.values.flatten())
        m.update(self.labels.values.flatten())
        m.update(additional_input.encode())
        result = m.hexdigest()
        return result #str(hashlib.md5((str(self.truth)+str(self.injected)+str(self.labels)+str(additional_input)).encode()).hexdigest())


    @property
    def original_scores(self):
        from Repair.estimator import Estimator
        return Estimator().scores(self.injected,self.truth,self.injected_columns,self.labels,predicted=self.injected)