import numpy as np
import sklearn.metrics as sm


class DataPart:
    def __init__(self, injected, original,train, name , a_type ):
        assert isinstance(a_type,str)
        assert injected.shape == original.shape
        assert injected.shape[0] > 100 , injected.shape
        assert injected.shape[1] > 2 , injected


        self.original_ = original.reset_index(drop=True)
        self.injected_ = injected.reset_index(drop=True)
        assert not np.allclose(injected.values,original.values)

        self.class_ = self.original_.ne(self.injected_)  ## important to drop colums
        injected_bool = self.class_.any()
        self.injected_columns = np.arange(len(injected_bool))[injected_bool]

        for col in self.injected_columns:
            assert np.any(self.class_.values[:, col]) , "AAAAA"

        for col in self.injected_columns:
            x = np.array(self.injected_)[:, col]
            truth = np.array(self.original_)[:, col]
            assert not np.allclose(x, truth)




        first_col = self.class_.iloc[:,0].values
        self.train_: DataPart = train
        self.generate_labels()

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

        return DataPart(self.injected.iloc[:, columns], self.truth.iloc[:, columns], cutted_train , a_type=self.a_type,name=self.name)

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


    def generate_column_labels(self,class_column, column_index , label_ratio=0.2, label_anom_start=0.8):

        state = np.random.get_state()
        np.random.seed(100)

        for i in range(1000):
            starts = [min(r) for r in DataPart.get_anomaly_ranges(class_column) if len(r) > 1]
            m = len(class_column)
            r_number = np.random.uniform(size=m)
            r_number[starts] = r_number[starts] < label_anom_start
            r_number = r_number > 1 - label_ratio
            labels = r_number.astype(bool)
            if column_index not in self.injected_columns:
                break

            if np.any((class_column.astype(int) - labels)> 0 ): # make there are non labeled data points
                break

        np.random.set_state(state)
        #check for non zero weights



        if column_index in self.injected_columns:
            assert np.any((class_column.astype(int) - labels)> 0 ) , "labeled all anomalies there will be no weights"
        return labels

    def generate_labels(self):
        self.labels = self.class_.copy()
        for  i, column_name in enumerate(self.labels):
            self.labels[column_name] = self.generate_column_labels(self.labels[column_name],i)

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
        }

        self.repairs[repair_name] = repair_dict

        repair_metrics = repair_results["scores"]
        repair_metrics["runtime"] = repair_results["runtime"]

        self.repair_metrics[(repair_name, repair_type)] = repair_metrics


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

    def check_weights(self):
        assert sum(self.get_weights()) != 0


    def check_original_rmse(self):
        assert np.any(self.class_.values)
        weights = np.zeros_like(self.injected.values)
        weights[self.class_] = 1
        weights[self.labels] = 0
        weights = weights.flatten()

        assert np.any(weights)
        injected_np = self.injected.values.flatten()
        truth_np = self.truth.values.flatten()

        original_rmse = sm.mean_squared_error(truth_np, injected_np, sample_weight=weights)