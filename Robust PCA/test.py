# generate low rank synthetic data
# we need structure in the data e.g weeks
import numpy as np
import matplotlib.pyplot as plt
from Robust_PCA import R_pca

N = 20
num_groups = 3
num_values_per_group = 10
p_missing = 0.2

Ds = []
for k in range(num_groups):
    d = np.ones((N, num_values_per_group)) * (k + 1) * 10
    Ds.append(d)

D = np.hstack(Ds)

# decimate 20% of data
n1, n2 = D.shape
S = np.random.rand(n1, n2)
D[S < 0.2] = 0
print(D.shape)
# use R_pca to estimate the degraded data as L + S, where L is low

rpca = R_pca(D)
L, S = rpca.fit(max_iter=10000, iter_print=100)
print(D)
print(L)
print(S)
plt.plot(D)
plt.show()
plt.plot(L)
plt.show()
plt.plot(S)
plt.show()
# visually inspect results (requires matplotlib)
rpca.plot_fit()
plt.show()