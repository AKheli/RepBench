import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def __init__(self, delta):
    assert isinstance(delta, Number)
    assert float(delta) >= 0, 'delta has to be non-negative.'

    self.delta = float(delta)
    self.delta_half_square = (self.delta ** 2) / 2.



def my_RPCA(injected, delta , n_components , cols = -1):
    error_tol = 0.00000001
    iterations = 100
    n_samples, n_features = X.shape

    def call(self, x):
        x_flt = x
        result = np.zeros_like(x_flt)
        result[x_flt < self.delta] = (x_flt ** 2) / 2.
        result[x_flt >= self.delta] = delta * x_flt - self.delta_half_square
        return result

    def weight(self, x):
        x_flt = x
        assert all(x_flt >= 0)
        result = np.ones_like(x)
        result[x >= delta] = x_flt*1/delta
        return result

    weights_ = 1. / n_samples * np.ones(n_samples)

    for i in range(iterations):
        # Calculating components with current weights
        self.mean_ = np.average(X, axis=0, weights=self.weights_)
        X_centered = X - self.mean_
        x = X_centered * np.sqrt(self.weights_.reshape(-1, 1))

        U, S, V = linalg.svd(x)
        # sorted eigenvectors
        self.components_ = V[:n_components, :]

        # X_rec = self.inverse_transform(self.transform(X))
        #
        #
        # h = np.array(np.linalg.norm(X-X_rec,axis=1))
        # delta = self.loss.delta
        # leq = np.array(h<= delta,dtype=bool)
        #
        # h[leq] = h[leq]**2/2
        # h[np.invert(leq)] = h[np.invert(leq)]*delta-delta**2/2
        # huber_loss = abs(0)
        # print("huber_loss", sum(h))

        # Calculate current errors in different models
        if self.model == 'first':

            non_projected_metric = np.eye(n_features) - \
                                   self.components_.T.dot(self.components_)

            # np.sqrt(np.diag(X_centered.dot(non_projected_metric.dot(X_centered.T))))
            #

            diff = X_centered - np.dot(X_centered, self.components_.T).dot(self.components_)
            if self.col != -1:
                diff = diff[:, :self.col]
            errors_raw = np.linalg.norm(diff, axis=1)
            # errors_raw = np.sqrt(np.diag(X_centered.dot(non_projected_metric.dot(X_centered.T))))
        elif self.model == 'second':
            # Obtain inverse empirical covariance from the SVD
            R_inv = np.diag(1. / S ** 2.)
            inverse_cov = V.T.dot(R_inv.dot(V))
            errors_raw = np.sqrt(np.diag(X_centered.dot(inverse_cov.dot(X_centered.T))))
        else:
            raise ValueError('Model should be either \"first\" or \"second\".')
        # errors_raw[errors_raw == np.nan] = 0

        errors_loss = vectorized_loss(errors_raw)
        # New weights based on errors
        self.weights_ = vectorized_weights(errors_raw)
        self.weights_ /= self.weights_.sum()
        # Checking stopping criteria
        self.n_iterations_ += 1
        old_total_error = self.errors_[-1]
        total_error = errors_loss.sum()

        if not np.equal(total_error, 0.):
            rel_error = abs(total_error - old_total_error) / abs(total_error)
        else:
            rel_error = 0.

        logging.debug('[RPCA] Iteraton %d: error %f, relative error %f' % (self.n_iterations_,
                                                                           total_error,
                                                                           rel_error))
        self.errors_.append(total_error)
        not_done_yet = rel_error > self.eps and self.n_iterations_ < 100  # self.max_iter

    if rel_error > self.eps:
        warnings.warn('[RPCA] Did not reach desired precision after %d iterations; relative\
                      error %f instead of specified maximum %f' % (self.n_iterations_,
                                                                   rel_error,
                                                                   self.eps))
    # Get variance explained by singular values
    explained_variance_ = (S ** 2) / n_samples
    total_var = explained_variance_.sum()
    if not np.equal(total_var, 0.):
        explained_variance_ratio_ = explained_variance_ / total_var
    else:
        explained_variance_ratio_ = np.zeros_like(explained_variance_)
    self.n_samples_, self.n_features_ = n_samples, n_features
    self.n_components_ = n_components
    self.explained_variance_ = explained_variance_[:n_components]
    self.explained_variance_ratio_ = \
        explained_variance_ratio_[:n_components]

    self.errors_ = np.array(self.errors_[1:])

    m = 8
    delta = 0.5
    def c_x_bar(wk,x):
        return np.dot(wk,x)/sum(wk)

    def c_H_k(wk,x_bar,x):
        dif = x - x_bar
        return(np.dot((wk*dif.T) ,dif)/sum(wk))

    def tk(C,x,b):
        return np.dot(C,x.T).T-b

    def w_k(t_k):
        t_k_norm = np.linalg.norm(t_k,axis=1)
        result = np.ones_like(t_k_norm)
        result[t_k_norm > delta] = delta/np.linalg.norm(t_k_norm[t_k_norm>delta])
        return result

    mean =  np.mean(x,axis=0)
    x = x - mean
    #init values
    x_bar = np.mean(x,axis=0)
    dif = x-x_bar
    H= np.dot(dif.T,dif)
    eigen_vectors = np.linalg.eig(H)[1][::-1]
    C = eigen_vectors[:m]
    b = np.dot(C,x_bar.T)


    for i in range(100):
        tk_ = tk(C,x,b)
        assert tk_.shape[0] == x.shape[0]
        wk = w_k(tk_)
        x_bar = c_x_bar(wk,x)
        H = c_H_k(wk,x,x_bar)
        eigen_vectors = np.linalg.eig(H)[1][::-1]
        C = eigen_vectors[:m]
        b = np.dot(C, x_bar.T)

    principal_components = eigen_vectors[:m]
    #transform
    transformed = np.dot(np.array(injected)-mean,principal_components.T)
    result  = np.dot(transformed, principal_components)+mean

    injected.plot()
    cols = list(injected.columns)
    result = pd.DataFrame(data=result)
    result.columns = cols
    result.plot()
    plt.show()
    return {"repair" : result}