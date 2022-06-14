import numpy as np
from numpy.linalg import LinAlgError


def imr(x, y_k, labels, tau=0.1, p=1, k=2000):
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

        elements = mod_range[(np.abs(y_hat - yvec) >= tau) * shifted_non_labelled]
        try:
            index = elements[np.argmin(np.abs( y_hat[elements] )) ]
        except ValueError as e:
            #print(f'terminated after {i} iterations')
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

# labels = [0, 1, 2, 5,8,11,22] #in the paper add +1
# x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9,  6.3, 6.8, 7.5, 8.5,6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9,  6.3, 6.8, 7.5, 8.5])
# y_k = np.array([6, 5.6, 5.4, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5,6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9,  6.3, 6.8, 7.5, 8.5])
# y= y_k.copy()
#
# result = imr2(x,y_k,labels=np.array(labels))["repair"]
# print(result)

# plt.plot(x,label = "dirty")
# plt.plot(result,label = "rep")
# plt.plot(y,label = "y")
# plt.legend()
# plt.show()