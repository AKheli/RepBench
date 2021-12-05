
import numpy as np
import pandas as pd
import scipy
from numpy.linalg import LinAlgError
from statsmodels.regression.linear_model import OLS
import matplotlib.pyplot as plt
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

def ols(yvec,xMat):
    nonzeros = np.unique(np.nonzero(xMat)[0])
    return np.linalg.lstsq(xMat[nonzeros,:],yvec[nonzeros],rcond=-1)[0]





def ols_direct(yvec, xMat):
    try:
        return np.dot(np.linalg.inv(np.dot(xMat.T, xMat)), np.dot(xMat.T, yvec))
    except:
        return np.zeros(len(xMat[0,:]))

def ols_direct_2(yvec, xMat):
    try:
        return np.linalg.inv(xMat.T.dot(xMat)).dot(xMat.T.dot(yvec))
    except:
        return np.zeros(len(xMat[0, :]))







def imr2(x,y_k,labels,tau=0.1,p=1,k=2000):
    z = np.array(y_k,dtype=np.single) - np.array(x,dtype=np.single)
    yvec = z[p:]

    mod_length = len(x) - p

    xMat = np.zeros((mod_length, p),dtype=np.single)

    shifted_non_labelled = np.ones(len(x)-p,dtype=bool)
    shifted_non_labelled[ (labels-p)[(labels-p) >= 0]] = False  #  if i + p not in labels:
    iterations = 0

    mod_range = np.arange(mod_length)

    for i in range(len(x) - p):
        for j in range(p):
            xMat[i, j] = z[p + i - j - 1]

    for i in range(k):
        try:
            phi =  np.linalg.inv(xMat.T.dot(xMat)).dot(xMat.T.dot(yvec))
        except:
            phi =  np.zeros(len(xMat[0, :]))

        y_hat = xMat.dot(phi)


        #assert np.allclose(phi,ols_direct(yvec, xMat), atol=1e-04)

        elements = mod_range[(np.abs(y_hat - yvec) >= tau) * shifted_non_labelled]
        try:
            index = elements[ np.argmin(np.abs( y_hat[elements] ),) ]
        except ValueError as e:

            print(f'terminated after {i} iterations')
            break
        val = y_hat[index]
        yvec[index] = val

        iterations = i
        for j in range(p):
            if index + 1 + j >= mod_length:
                break
            if index + 1 + j < 0:
                continue
            xMat[index + 1 + j, j] = val

    modify = x.copy()
    modify[labels] = y_k[labels]
    for i in range(len(modify)):
        if i not in labels:
            modify[i] = x[i] + yvec[i - p]

    return { "repair" : modify , "iterations"  : iterations , "max_iterations" :k , "tau" : tau , "p" : p , "labels" : labels}

def imr(x,y_k,labels,tau=0.1,p=1,k=2000):
    z = np.array(y_k) - np.array(x)
    yvec = z[p:]
    xMat = np.zeros((len(x)-p,p))

    for i in range(len(x)-p):
        for j in range(p):
            xMat[i,j] = z[p + i - j - 1]

    for j in range(k):
        phi = ols(yvec,xMat)
        y_hat = xMat.dot(phi)
        #print("phi",phi)
        residuals = y_hat-yvec
        abs_res = np.abs(residuals)
        minA = 100000000000
        index = -1
        for i in np.arange(len(x)-p):
            if i +p in labels:
                continue
            if abs_res[i] < tau:
                continue
            y_hat_point = np.abs(y_hat[i])
            if(y_hat_point < minA):
                minA = y_hat_point
                index = i
        #print(index)
        if index == -1:
            print(f'terminated after {j} iterations')
            break
        #print(index)
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
    #print("AAAAA")
    #print("suum",sum(modify - imr2(x,y_k,labels,tau=tau,p=p,k=k)))
    #assert np.allclose(modify, imr2(x,y_k,labels,tau=tau,p=p,k=k))
    return modify


def IMRsave(index,x,y_o,truth,labels,repair,name , arrows = True):
    frame = pd.DataFrame(x)
    frame["y_o"] = y_o
    frame["truth"] = truth
    frame ["labels"] = [i in labels for i in range(len(x))]
    frame["repair"] = repair
    #print(frame)
    frame.to_csv("Data/IRMSAVE/"+name)

def plot(injected,repair={},truth=[],title = "",labels = [], index=None , arrows = False ,show = True , observation_rms = ""):
    injected =np.array(injected)
    truth =np.array(truth)

    if index is None:
        index = np.array(range(len(truth)))

    #print(labels)
    #print(index[labels])

    plt.plot(index,injected, label="anomaly"+observation_rms ,linestyle = "--",marker = "x", color= "red",lw=1)
    plt.title(title)


    markers = [ "s" , "P" ,"+" ,"<",">","8","p"]
    if isinstance(repair, dict):
        for key , value  in  repair.items():
            plt.plot(index,value, label=key , marker = markers.pop()  ,mfc='none') #,markersize=10)
    else:
        plt.plot(index, repair, label="repair",marker = 'x')


    plt.plot(index, truth, label="truth", color="black" , lw=3)
    plt.plot(index[labels], truth[labels], 'o', mfc='none', label="labels",markersize=8,color="green")

    if arrows:
        mask = (abs(repair - injected)) > 0.01
        for i in index[mask]:
            plt.arrow(index[i],repair[i],0, injected[i]-repair[i] ,color = "grey" , alpha=0.2,ls = '--' , length_includes_head = False)
    #plt.legend()
    plt.grid(alpha = 0.2)
    #plt.xlim( np.arange(len(repair))[truth != repair] )
    if show :
        plt.draw()
        plt.show()
    else:
        plt.legend(bbox_to_anchor=(0., -0.25, 1., 0.00), loc='lower left',
                   ncol=3, mode="expand", borderaxespad=0.)
        plt.subplots_adjust(bottom=0.2 , top = 0.92)
        return plt



