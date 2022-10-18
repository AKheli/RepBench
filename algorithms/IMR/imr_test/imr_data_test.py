import time

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TKAgg')

df = pd.read_csv("ild3k.data" , header=None)



# tau = 0.1 in the paper
tau  =0.1
injected = df.iloc[:,1].values
std = np.std(injected)
print(tau/std)
print(0.05/std)

y_0 = df.iloc[:,2].values
anomalies = (injected - y_0)[~(injected==y_0)]
print("mean anomalies" , np.mean(abs(anomalies/(std))))



