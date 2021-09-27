

from scipy.linalg import lstsq as ls
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression as LR


x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
labels = [0,1,2,5,11]


x[labels] = y[labels]

x_right = x[1:]
x_left = x[:-1]

tau = 0.1

D = np.concatenate( (np.zeros(len(x_left)),x_left) ,axis=0 ).reshape(2,-1).T



theta  = ls(D,x_right)[0]

fitted = theta[0]+x_left*theta[1]
absres = abs(x_right-fitted)

print(10)

for i in range(1,len(x_right)):
    x_right[i]
    print(i)
    if abs(x[i]  - (x_left[i-1]*theta[1]  +theta[0]       ) ) > tau and i not in labels:
        print(x_right[i-1] , fitted[i-1])
        x[i] = x_left[i-1]*theta[1]

y = x

# {6, 5.6, 5.4, 5.52, 5.64, 5.4, 5.6, 5.72, 5.84, 5.97, 6.10, 8.5}.

