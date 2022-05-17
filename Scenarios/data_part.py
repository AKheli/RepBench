import numpy as np
import sklearn.metrics as sm


class DataPart:
    def __init__(self, injected, original, train=None):
        assert injected.shape == original.shape
        assert injected.shape[0] > 100 , injected.shape
        assert injected.shape[1] > 2
        self.original_ = original.reset_index(drop=True)
        self.injected_ = injected.reset_index(drop=True)
        self.class_ = self.original_.ne(self.injected_)  ## important to drop colums
        self.train_: DataPart = train
        injected_bool = self.class_.any()
        self.injected_columns = np.arange(len(injected_bool))[injected_bool]
        self.generate_labels()

        if train is not None:
            assert train.train is None

        self.repairs = {}
        self.repair_names = []
    @property
    def truth(self):
        return self.original_

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

    def get_cutted(self, columns):
        if isinstance(columns, int):
            columns = np.arange(columns)

        cutted_train = None
        if self.train is not None:
            cutted_train = self.get_cutted(columns)

        return DataPart(self.injected.iloc[:, columns], self.injected.iloc[:, columns], cutted_train)

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

    @staticmethod
    def generate_column_labels(class_collumn, label_ratio=0.2, label_anom_start=0.8):
        starts = [min(r) for r in DataPart.get_anomaly_ranges(class_collumn) if len(r) > 1]
        m = len(class_collumn)
        r_number = np.random.uniform(size=m)
        r_number[starts] = r_number[starts] < label_anom_start
        r_number = r_number > 1 - label_ratio
        return r_number.astype(bool)

    def generate_labels(self):
        self.labels = self.class_.copy()
        for column_name in self.labels:
            self.labels[column_name] = DataPart.generate_column_labels(self.labels[column_name])

    @property
    def repair_inputs(self):
        return {"injected": self.injected,
                "truth": self.truth,
                "labels": self.labels,
                "injected_columns": self.injected_columns,
                "score_indices" : self.get_weights()}

    def add_repair(self, repair_results, repair_name: str):
        assert repair_name not in self.repairs , f" {repair_name} already in {self.repairs.keys()}"
        f"such a repair already exists:{repair_name}"
        self.repair_names.append(repair_name)

        repair = repair_results["repair"]
        assert repair.shape == self.labels.shape , (repair_name,repair.shape , self.labels.shape ,self.truth.shape, self.injected.shape)
        ### compute errors

        weights = np.zeros_like(repair.values)
        weights[:, self.injected_columns] = 1
        weights[self.labels] = 0
        weights = weights.flatten()

        repair_np = repair.values.flatten()
        injected_np = self.injected.values.flatten()
        truth_np = self.truth.values.flatten()
        assert sum(weights) != 0 ,self.injected.values
        original_rmse = sm.mean_squared_error(truth_np, injected_np, sample_weight=weights)
        repair_rmse = sm.mean_squared_error(truth_np, repair_np, sample_weight=weights)

        original_mae = sm.mean_absolute_error(truth_np, injected_np, sample_weight=weights)
        repair_mae = sm.mean_absolute_error(truth_np, repair_np, sample_weight=weights)


        # on amomalies only
        class_labels = self.klass.values
        class_labels[self.labels] = False
        class_labels = class_labels.flatten().astype(int)

        original_anomaly_rmse = sm.mean_squared_error(truth_np, injected_np, sample_weight=class_labels)
        repair_anomaly_rmse = sm.mean_squared_error(truth_np, repair_np, sample_weight=class_labels)

        repair_dict = {
            "repair": repair_results["repair"],
            "name": repair_results["name"],
            "original_rmse": original_rmse,
            "repair_rmse": repair_rmse,
            "original_mae": original_mae,
            "repair_mae": repair_mae,
            "original_anomaly_rmse": original_anomaly_rmse,
            "repair_anomaly_rmse": repair_anomaly_rmse,
            "runtime" : repair_results["runtime"]
        }


        self.repairs[repair_name] = repair_dict

    def get_errors(self,error_name = "rmse" ):
        if error_name == "rmse":
            name = "repair_anomaly_rmse"
            original_name = "original_anomaly_rmse"

        return { k : v[name]  for k,v  in self.repairs.items()}


    def get_weights(self):
        weights = np.zeros_like(self.injected_.values)
        weights[:, self.injected_columns] = 1
        weights[self.labels] = 0
        weights = weights.flatten()
        return weights