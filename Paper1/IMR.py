
import numpy as np
from statsmodels.regression.linear_model import OLS




def ols(respond,x , c = 0, p = 1):
    # [ 0 , x[1:-p+1] , x[2:-p+2] ]
    X = np.array( [ np.repeat(c,len(x)-p) ] +  [ x[i: -p+i] for i in range(0,p)] ).T
    return OLS(respond[p:], X).fit().params[1]

##AR  c = 0 Example 1
x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5] )
y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5]) #  x4 and x5 unlabeled , #y7′ . . . y11 ′ ,  unlabeled
labels = [0, 1, 2, 5,11] #in the paper add +1
x[labels] = y[labels]
tau  = 0.1
phi = ols(x,x)
x_prime = x.copy()

for i in range(1,len(x)):
    if i not in labels and abs(x_prime[i]-x_prime[i-1]*phi) > tau:
        x_prime[i] = x_prime[i-1]*phi


## ARX

def ARX(x, y, labels):
    y_prime = x.copy()
    y_prime[labels] = y[labels]
    tau = 0.1

    phi = ols(y_prime - x, y_prime - x)

    print(y)
    print(phi)
    for i in range(1, len(x)):
        predicted = x[i] + (y[i - 1] - x[i - 1]) * phi
        if i not in labels and abs(y[i] - x[i]) > tau:
            y[i] = predicted
    return y

x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5] )
y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5]) #  x4 and x5 unlabeled , #y7′ . . . y11 ′ ,  unlabeled
labels = [0, 1, 2, 5,11] #in the paper add +1

arx = ARX(x,y,labels)
print(arx , "arx result")

##iterative

x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5] )
y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5]) #  x4 and x5 unlabeled , #y7′ . . . y11 ′ ,  unlabeled
labels = [0, 1, 2, 5,11] #in the paper add +1


y_k = x.copy()
y_k[labels] = y[labels]

for j in range(6):
    phi = ols(y_k - x, y_k-x)
    candidate  = y_k.copy()
    for i in range(1,len(candidate)):
        candidate[i] = x[i]+phi*(y_k[i-1]-x[i-1])

    diff = abs(candidate-x)
    diff[labels] = 100000
    diff[abs(candidate-y_k) < tau] = 1000000
    if (max(diff) < tau):
        print(j)
        print("all small enough")
        break
    maxindex = np.argmin(diff)
    y_k[maxindex] = candidate[maxindex]

print(y_k)
y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5]) #  x4 and x5 unlabeled , #y7′ . . . y11 ′ ,  unlabeled
print(    (np.mean(np.square(y_k-y)))**(1/2) )