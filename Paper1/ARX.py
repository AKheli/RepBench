##ARX example from the paper

from scipy.linalg import lstsq as ls
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression as LR


#y = theta*[0,X]
def OLS(x,y, p = 1,c = 0):
    D = np.concatenate((np.zeros(len(x)), x), axis=0).reshape(p+1, -1).T
    print(x)

    print(D)
    theta = ls(D, y)[0]
    return theta

def ARX_labeled_OLS( x,ylabeled, labels , p = 2,c = 0 ):
    x[labels] = ylabeled[labels]
    x_right = np.concatenate([ylabeled[i:] - x[i:] for i in range(1,p+1)])
    x_left = (ylabeled - x)[:-1]
    return OLS(x_right ,x_left ,p,c)



if __name__ == '__main__':
    x_original = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
    x = x_original.copy()
    y = np.array([6, 5.6, 5.4, 5.2, 5.4, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
        labels = [0,1,2,5,11]

    theta = ARX_labeled_OLS(x,y ,labels)   #problem here is the fit rouned ?
    phi = theta[1]

    tau = 0.1
    x = x_original


    print(10)

    for i in range(1,len(x)):
        if  i not in labels:
            y_prime = x[i]+phi*(y[i-1] - x[i-1])
            if i == 3:
                print(y_prime , "y3" ,  x[i-1] , y[i-1] , "xi" , x[i])
            if abs(phi*(theta[1] + theta[0])) > tau :
                y[i] = y_prime

    #y = x

    # {6, 5.6, 5.4, 5.52, 5.64, 5.4, 5.6, 5.72, 5.84, 5.97, 6.10, 8.5}.


