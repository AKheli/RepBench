import warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from recommendation.feature_extraction.feature_extraction import feature_endings
from recommendation.utils import *


class RecommendationInputLoader:
    feature_folder = "recommendation/results/features"
    all_features = list(feature_endings.values())

    def __init__(self,
                 feature_file_name="results_features_non_normalized",
                 train_split_r=0.8,
                 features="all",
                 nan_safe=True,
                 include_anomaly_infos=False):

        if features == "all":
            features = self.all_features
        else:
            assert isinstance(features, list), "features must be a list of feature names"
            assert all([f in self.all_features for f in features]), f"features must be a subset of {self.all_features}"

        self.feature_file_name = feature_file_name
        self.feature_file_path = f"{self.feature_folder}/{feature_file_name}"
        self.train_split_r = train_split_r

        np.random.seed(0)

        algorithms_scores = parse_recommendation_results(self.feature_file_path)
        self.best_algorithms = algorithms_scores['best_algorithm']
        self.best_algorithms = self.best_algorithms.values.flatten()
        self.feature_values = algorithms_scores['features'].copy()

        all_close = lambda col: np.allclose(col.values, col.values[0])

        self.feature_names = [f_name for f_name in self.feature_values.columns
                              if any([f_name.endswith(f) for f in features])
                              and not all_close(self.feature_values[f_name])
                              ]

        print(f"used features: {self.feature_names}")

        self.feature_values = self.feature_values[self.feature_names]

        ## add anomaly infos as a feature:
        if include_anomaly_infos:
            injection_params = algorithms_scores['injection_parameters']
            a_type = injection_params['a_type']
            factor = injection_params['factor']
            a_percent = injection_params['a_percent']
            # self.feature_values['a_type'] = a_type
            self.feature_values["factor"] = factor.to_list()
            self.feature_values['a_percent'] = a_percent.iloc[:].values

        encoder = LabelEncoder()
        self.categories_encoded = encoder.fit_transform(self.best_algorithms)
        self.encoder = encoder
        self.labels = encoder.classes_
        # remove features with nan entries
        if nan_safe:
            nan_free_rows = ~np.isnan(self.feature_values.values).any(axis=1)
            self.feature_values = self.feature_values.iloc[nan_free_rows, :]
            self.categories_encoded = self.categories_encoded[nan_free_rows]

        ## Split data into train and test sets
        n_train_split = int(len(self.feature_values) * train_split_r)
        train_split = np.random.choice(len(self.feature_values), n_train_split, replace=False)
        test_split = np.setdiff1d(np.arange(len(self.feature_values)), train_split)

        self.X_train: pd.DataFrame = self.feature_values.iloc[train_split, :]
        self.X_test: pd.DataFrame = self.feature_values.iloc[test_split, :]
        self.y_train, self.y_test = self.categories_encoded[train_split], self.categories_encoded[test_split]

        # check for NaN values
        assert not np.isnan(self.X_test.values).any(), self.X_test
        assert not np.isnan(self.X_train.values).any(), self.X_train

    def encode(self, y):
        return self.encoder.transform(y)

    def decode(self, y):
        return self.encoder.inverse_transform(y)
