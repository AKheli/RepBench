from scipy import linalg
from sklearn.decomposition import TruncatedSVD
from sklearn.utils import check_array

import numpy as np


def compute_components_(centered_weighted_x, n_components, component_method="TruncatedSVD"):
    if component_method == "TruncatedSVD":
        tsvd = TruncatedSVD(n_components=n_components)
        tsvd.fit(centered_weighted_x)
        components = tsvd.components_
        return components

    U, S, V = linalg.svd(centered_weighted_x)
    components = V[:n_components, :]
    return components


def fit_components(matrix, n_components , delta , max_iter  = 20):
    X = check_array(matrix, dtype=[np.float32], ensure_2d=True,
                    copy=True)

    n_samples, n_features = X.shape

    weights = 1. / n_samples * np.ones(n_samples)

    n_iterations_ = 1
    not_done_yet = True

    last_error = np.inf
    while not_done_yet:
        mean = np.average(X, axis=0, weights= weights)
        X_centered = X - mean
        C = compute_components_(X_centered * np.sqrt(weights.reshape(-1, 1)),n_components)

        diff = X_centered - np.dot(X_centered, C.T).dot(C)
        errors_raw = np.linalg.norm(diff, axis=1)
        errors_loss = compute_loss(errors_raw,delta)
        total_error = errors_loss.sum()

        weights = compute_weights(errors_raw,delta)
        weights /= weights.sum()
        n_iterations_ += 1

        not_done_yet = n_iterations_ < max_iter  #or abs(total_error - old_error) / abs(total_error)

    return C





def compute_loss(x,delta):
    delta_half_square = (delta ** 2) / 2.
    smaller = x <= delta
    bigger = np.invert(smaller)
    result = np.zeros_like(x)
    result[smaller] = x[smaller] ** 2 / 2.
    result[bigger] = delta * x[bigger] - delta_half_square
    return result


def compute_weights(x,delta):
    return 1.0*(x<delta)+((x>=delta)/x)
