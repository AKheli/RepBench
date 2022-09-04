import numpy as np
def local_sign_vector_init_speed_up(double[:, :] matrix, double[:] z ):
    cdef double[:] Z = z.copy()
    cdef double[:] direction = matrix[0].copy()
    cdef double gradPlus = 0.0
    cdef double gradMinus = 0.0
    cdef double[:] neg_row
    cdef int i = 1
    cdef int n = matrix.shape[0]
    while i < n:
        row = matrix[i,:]
        neg_row = np.negative(row)
        gradPlus = np.sum((np.add(direction,row))**2)
        gradMinus = np.sum((np.add(direction,neg_row))**2)

        if gradMinus > gradPlus:
            Z[i] = -1

        direction += np.multiply(Z[i],row)
        i +=1
    return Z