
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS
import matplotlib.pyplot as plt



def ols(respond,x , p = 1, c = 0):
    # [ 0 , x[1:-p+1] , x[2:-p+2] ]
    X = np.zeros((len(x),p+1))
    X[:,0] = c
    for i in range(1,p+1):
        X[i:,i] = x[:-i]
    X = X[p:,:]

    #X = np.array( [ np.repeat(c,len(x)-p) ] +  [ x[i: -p+i] for i in range(0,p)] ).T
    #print(X,"before")
    return OLS(respond[p:], X).fit().params[1:]

def paramestimation(x,y_k,p=1):
    return ols(y_k - x, y_k - x,p)

def candidategeneration(x,y_k,phi):
    y_hat = np.zeros(len(x.copy()))
    phi = np.array(phi,ndmin=1)
    for i in range(1,len(phi)+1):
        y_hat[i:] += phi[i-1]*(y_k-x)[:-i]
    return y_hat

def candidates(y_k,y_hat,labels,tau):
    diff = abs(y_k-y_hat)
    diff[labels] = 0
    return y_hat[diff>tau] , np.arange(len(y_hat))[diff>tau]

def repair_value_index(y_hat,x,indices):
    #print(indices)
    #print(np.argmin(abs(y_hat-x)[indices]))
    argm = indices[np.argmin(abs(y_hat-x)[indices])]
    return y_hat[argm] ,argm

##iterative


# labels = [0, 1, 2, 5,8,11] #in the paper add +1
# x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 16.3, 20.8,
# 7.5, 8.5])
# y_k = np.array([6, 5.6, 5.4, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
# y= y_k.copy()


def imr(x,y_k,labels,tau=0.1,p=1,k=2000):
    z = np.array(y_k) - np.array(x)
    yvec = z[p:]
    xMat = np.zeros((len(x)-p,p))
    for i in range(len(x)-p):
        for j in range(p):
            xMat[i,j] = z[p + i - j - 1]

    for i in range(k):
        phi = OLS(yvec,xMat).fit().params
        y_hat = xMat.dot(phi)
        print("phi",phi)
        residuals = y_hat-yvec
        abs_res = abs(residuals)
        minA = 100000000000
        index = -1
        for i in range(len(x)-p):
            if i +p in labels:
                continue
            if abs_res[i] < tau:
                continue
            y_hat_point = abs(y_hat[i])
            if(y_hat_point < minA):
                minA = y_hat_point
                index = i
        if abs_res[index] == 100000000000 :
            print(f'terminated after {i} iterations')
            break
        print(index)
        val = y_hat[index]
        yvec[index] = val
        for j in range(p):
            if index +1+j >= len(x)-p:
                break
            if index +1+j < 0:
                continue
            xMat[index +1+j, j] = val

    modify = x.copy()
    modify[labels] = y_k[labels]
    for i in range(len(modify)):
        if i not in labels:
            modify[i] =x[i]+ yvec[i-p]

    return modify


def IMRsave(index,x,y_o,truth,labels,repair,name , arrows = True):
    frame = pd.DataFrame(x)
    frame["y_o"] = y_o
    frame["truth"] = truth
    frame ["labels"] = [i in labels for i in range(len(x))]
    frame["repair"] = repair
    #print(frame)
    frame.to_csv("data/IRMSAVE/"+name)

def plot(injected,repair,truth,labels,title, index=None , arrows = False ,show = True):
    injected =np.array(injected)
    repair =np.array(repair)
    truth =np.array(truth)

    if index is None:
        index = np.array(range(len(repair)))
    plt.plot(index,injected, 'x', label="injected")
    plt.title(title)
    plt.plot(index,truth, label="truth")
    plt.plot(index, repair, 'o', label="repair")
    plt.plot(index[labels], truth[labels], 'o', label="labeled", )
    if arrows:
        mask = (abs(repair - injected)) > 0.01
        for i in index[mask]:
            plt.arrow(index[i],repair[i],0, injected[i]-repair[i] ,color = "grey" , alpha=0.2,ls = '--' , length_includes_head = False)
    plt.legend()
    plt.grid(alpha = 0.2)

    if show :
        plt.show()
    else:
        return plt

