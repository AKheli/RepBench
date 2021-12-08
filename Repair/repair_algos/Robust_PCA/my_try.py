import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def my_RPCA(injected, **kargs):
    x = np.array(injected)

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