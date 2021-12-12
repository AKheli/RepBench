import numpy as np
import pandas as pd
import os

from Repair.repair_algos.Screen.Local import screen

print(os.listdir())
print(os.getcwd())
from Scenarios.metrics import RMSE



def search_s(data, truth):
    """
    data_df with row truth and injected to train on
    """
    anom = data != truth
    not_aom = data == truth

    dif = np.array(sorted(abs(np.diff(data[not_aom])), reverse=True))
    dif_anom = np.array(sorted(abs(np.diff(data[anom])) ,  reverse=True))
    np.arange(len(data))
    np.array((np.arange(len(data)), data) , dtype=np.float64)
    r  = lambda x : RMSE(screen(np.array((np.arange(len(data)), data), dtype=np.float64).T, SMIN = -x, SMAX = x)["repair"], truth)
    valmin , argmin = 100 , -1
    #print([ valmin ,argmin = (lambda x : (valmin , argmin) if x > valmin else (x  , i))(r(i))  for i in range(int(max(dif)))])
df = pd.read_csv("/".join(__file__.split("/")[:-1])+"/stock10k.data" , header = 0)
data = np.array(df["injected"])
truth = np.array(df["truth"])
s = search_s(data,truth)

