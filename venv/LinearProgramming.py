from scipy import optimize
import numpy as np


#
# x = np.array( (1,2,3,4,7,8,9,10))
# t = np.arange(10)+1
#
# smax = 0.5
# smin = -0.5
# w = 1
# #distance one for testing
# time_indices_i = [  a  for a,b in zip(t,t[1:]) if abs(a-b) <= w  ] #+  [  (a,b)  for a,b in zip(t,t[2:]) if abs(a-b) <= w  ]
# time_indices_j = [  b  for a,b in zip(t,t[1:]) if abs(a-b) <= w  ]
#
# A = np.zeros( (len(time_indices*2),  len(x)*2))
# print(A[time_indices_i])
#
#
#
#
# print(time_indices)
# #results = u,v
#
# def f(y):
#     return sum(np.abs(x-y))
# c = optimize.minimize(f,x ,bounds= bounds )
# print(c)



smax = 1
smin = 1
w = 1
x = np.array( (1,1.113,1.3,3,1,1,1))


# time_indices = [  (a,b)  for a,b in zip(t,t[1:]) if abs(a-b) <= w ] #+  [  (a,b)  for a,b in zip(t,t[2:]) if abs(a-b) <= w  ]
# A = np.eye(len(x)) - np.eye(len(x), k=1)
# numpy.concatenate(A,A)


A = np.eye(len(x)) - np.eye(len(x), k=1)
A = A[:-1,:]
print(A)
print(A.dot(x))

from scipy.optimize import LinearConstraint ,NonlinearConstraint
linear_constraint = NonlinearConstraint(lambda x : np.zeros(len(x)-1)+10, np.repeat(smin,len(x)-1), np.repeat(smax,len(x)-1))
def f(y):
     print(sum(np.abs(x-y)))
     return sum(np.abs(x-y))

def derivativef(y):
     return np.sign(x-y)


a = optimize.minimize(f,x, method='trust-constr' , constraints=[linear_constraint],  options= {"maxiter" : 10000, "disp" : True} )
print( A.dot(a.x) <= np.repeat(smax,len(x)-1))
print(x)
print(a.x)