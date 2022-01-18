# -*- coding: utf-8 -*-
# https://github.com/kirajcg/pymeboot/blob/master/pymeboot/meboot.py
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.experimental import enable_halving_search_cv  # noqa

from Injection.inject import scenario_inject
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.Scenario_Types import *
from data_methods.Helper_methods import get_df_from_file




def mean(L):
    return sum(L)/len(L)


def meboot(L, J=1):
    """
    Returns list of J maximum entropy bootstrap samples of time-series L
    """
    N = len(L)
    L_sort = sorted((e,i) for i,e in enumerate(L))
    L_vals = [l[0] for l in L_sort]
    L_inds = [l[1] for l in L_sort]
    L_out = [0]*J
    for j in range(J):
        Z = [(L_vals[i] + L_vals[i+1])/2 for i in range(N-1)]
        m_trm = mean([abs(L[i] - L[i-1]) for i in range(1, N)])
        Z = [L_vals[0] - m_trm] + Z + [L_vals[-1] + m_trm]
        m = [0]*N
        m[0] = 0.75*L_vals[0] + 0.25*L_vals[1]
        for k in range(1, N-1):
            m[k] = 0.25*L_vals[k-1] + 0.5*L_vals[k] + 0.25*L_vals[k+1]
        m[-1] = 0.25*L_vals[-2] + 0.75*L_vals[-1]
        U = sorted([random.random() for _ in range(N)])
        quantiles = [0]*N
        x = [float(y)/N for y in range(N+1)]
        for k in range(N):
            ind = min(range(len(x)), key=lambda i: abs(x[i] - U[k]))
            if x[ind] > U[k]:
                ind -= 1
            c = (2*m[ind] - Z[ind] - Z[ind + 1]) / 2
            y0 = Z[ind] + c
            y1 = Z[ind + 1] + c
            quantiles[k] = y0 + (U[k] - x[ind]) * \
                            (y1 - y0) / (x[ind + 1] - x[ind])
        L_out[j] = [x for y, x in sorted(zip(L_inds, quantiles))]
    return L_out


def meboot_np(L, J=1):
    """
    Returns list of J maximum entropy bootstrap samples of time-series L
    """
    L = np.array(L)
    N = len(L)
    assert L.ndim == 1
    sorted_indices = np.argsort(L)
    sorted_values = L[sorted_indices]
    L_out = [0]*J


    # N = len(L)
    # L_sort = sorted((e,i) for i,e in enumerate(L))
    # L_vals = [l[0] for l in L_sort]
    # L_inds = [l[1] for l in L_sort]

    Z = (sorted_values[:-1]+sorted_values[1:])/2
    m_trm = np.mean(np.abs(np.diff(sorted_values)))
    Z = np.array( [L[0] - m_trm] + list(Z) + [L[-1] - m_trm] )

    for j in range(J):
        #Z = [(L_vals[i] + L_vals[i+1])/2 for i in range(N-1)]
        #m_trm = mean([abs(L[i] - L[i-1]) for i in range(1, N)])
        #Z = [L[0] - m_trm] + Z + [L_vals[-1] + m_trm]
        m = np.zeros_like(L)
        m[0] = 0.75*sorted_values[0] + 0.25*sorted_values[1]
        # for k in range(1, N-1):
        #     m[k] = 0.25*L_vals[k-1] + 0.5*L_vals[k] + 0.25*L_vals[k+1]
        #
        m[1:-1] = 0.25*sorted_values[:-2] + 0.5*sorted_values[1:-1]+0.25*sorted_values[2:]
        m[-1] = 0.25*sorted_values[-2] + 0.75*sorted_values[-1]

        ###### onyl here the loop will be different?
        U = np.sort(np.random.uniform(size=N))

        quantiles = np.zeros(N)
        x = np.arange(N+1,dtype=float)/N #[float(y)/N for y in range(N+1)]
        counter = 0
        for k in range(N):
            u = U[k]

            try:
                while abs(x[counter+1]-u) <  abs(x[counter]-u):
                    counter += 1
            except:
                print("failed",counter,k)
                pass

            # ind = min(range(len(x)), key=lambda i: abs(x[i] - U[k]))
            # assert ind == counter

            ind = counter
            #print("passed")

            #ind = min(range(len(x)), key=lambda i: abs(x[i] - U[k]))
            if x[ind] > U[k]:
                ind -= 1
            c = (2*m[ind] - Z[ind] - Z[ind + 1]) / 2
            y0 = Z[ind] + c
            y1 = Z[ind + 1] + c
            quantiles[k] = y0 + (U[k] - x[ind]) * \
                            (y1 - y0) / (x[ind + 1] - x[ind])
        L_out[j] = [x for y, x in sorted(zip(sorted_indices, quantiles))]
    return L_out

data_file_name = "TemperatureTS8.csv"
injection_scenario = BASE_SCENARIO

df, name = get_df_from_file(data_file_name)
scenario_data = scenario_inject(df, injection_scenario, AMPLITUDE_SHIFT, train_split=0.5)


base_scenario = scenario_data["scenario_data"]["full_set"]
injected = base_scenario["injected"]
L = injected.iloc[:,0]
# x = meboot(L,1000)
# L  = pd.DataFrame(L)
# for i,t in enumerate(x):
#     L[i+1] = t
# L.plot()
# plt.show()

def conf_interval(ts,alpha,samples=10):
    x = np.array(meboot_np(ts, samples))
    upper = np.quantile(x,1-alpha/2,axis=0)
    lower = np.quantile(x,alpha/2,axis=0)
    # plt.plot(ts, label = "ts")
    # plt.plot(upper, label = "upper")
    # plt.plot(lower, label = "lower")
    # plt.legend()
    # plt.show()
    return lower, upper

def in_interval(injected,reduced,alpha,samples=100):
    injected = injected.copy()
    reduced = np.array(reduced)
    assert reduced.ndim == 1
    lower, upper  = conf_interval(reduced,alpha,samples)
    to_repair_values = np.logical_or(injected < lower , injected > upper)
    #print(to_repair_values)
    return to_repair_values