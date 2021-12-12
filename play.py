import numpy as np

x = np.arange(1,16,).reshape(3,-1)

c = np.array([[1,0,-1,0,20]])
c = c/np.sqrt(np.sum(c**2))
c = np.dot(c.T,c)

p = np.eye(5)-c
np.sqrt(np.diag(x.dot(p.dot(x.T)).T))
np.linalg.norm(x-np.dot(x,c.T),axis=1)