# generate low rank synthetic Data
# we need structure in the Data e.g weeks
import numpy as np
import matplotlib.pyplot as plt
from Robust_PCA import R_pca
import pandas as pd

file = "../../Data/YAHOO/YAHOO.csv"
df = pd.read_csv(file)

D  =np.array(df)

# decimate 20% of Data
n1, n2 = D.shape
S = np.random.rand(n1, n2)
#[S < 0.2] = 0
#print(D.shape)
# use R_pca to estimate the degraded Data as L + S, where L is low

rpca = R_pca(D)
L, S = rpca.fit(max_iter=100000, iter_print=100)

rpca.plot_fit()
plt.show()

L = L.reshape(-1)
treshhold = 7
#plt.plot(x, label = "injected")
plt.plot(L.reshape(-1), label = "L")
plt.plot(S,label = "S")
plt.legend()
plt.show()
