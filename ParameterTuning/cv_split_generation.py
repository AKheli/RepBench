import numpy as np
from sklearn.model_selection._split import _BaseKFold, BaseCrossValidator
from sklearn.utils.validation import _num_samples


class CV_splitter(BaseCrossValidator):
    def __init__(self, n_splits=5, random_state=None):
        self.n_splits = n_splits

    def _iter_test_indices(self, X, y=None, groups=None):
        n_samples = _num_samples(X)
        indices = np.arange(n_samples)
        splits = np.array_split(indices, self.n_splits)
        for split_range in splits:
            yield indices[split_range]

    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits
