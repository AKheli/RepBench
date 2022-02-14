import numpy as np
import scipy.optimize as opt
import scipy.sparse as sp
from timeit import default_timer as timer



# for time differences = 1 only
# time = None assume values with time differences of 1
def LPconstrainedAE(x, min=2, max=2, time=None, w=1, second=True , truth = None):
    n = len(x)
    uuncost = x.copy()
    c = np.ones(2 * n)

    if time is None:
        time = np.arange(n)

    A_ub = None
    b_ub = None

    time = np.array(time)
    i = 0
    while True:
        i = i + 1
        diff = time[i:] - time[:-i]
        if np.min(diff) > w:
            break
        else:
            mask = diff <= w
            # i difference  build the full matrix
            A = np.zeros((n - i, n), dtype=np.byte)
            A[np.arange(n - i), np.arange(n - i)] = 1
            A[np.arange(n - i), np.arange(i, n)] = -1

            A = A[mask, :]  # throw away the rows not contained the constraint

            B = np.concatenate((-A, A), axis=1, )
            B = np.concatenate((B, -B), axis=0, )

            xij = (x[:-i] - x[i:])
            b = np.concatenate((xij + max * diff, -xij + min * diff))
            b = b[np.concatenate((mask, mask))]

            if A_ub is None:
                A_ub = B
                b_ub = b
            else:
                A_ub = np.concatenate((A_ub, B), axis=0, )
                b_ub = np.concatenate((b_ub, b))


# else:
#     #one difference
#     A = np.zeros((n-1,n),dtype=np.byte)
#     A[np.arange(n-1),  np.arange(n-1) ] = 1
#     A[np.arange(n-1) ,  np.arange(1,n) ] = -1
#     B = np.concatenate((-A,A),axis=1, )
#     B = np.concatenate((B,-B),axis=0, )
#
#     xij = (x[:-1] - x[1:])
#     b = np.concatenate((xij+max,-xij+min),axis=0)
#
#     B = np.concatenate((-A, A), axis=1, )
#     B = np.concatenate((B, -B), axis=0, )
#
#     xij = (x[:-1] - x[1:])
#     b = np.concatenate((xij + max, -xij + min), axis=0)
#
#     # two difference
#     if second:
#         A2 = np.zeros((n - 2, n), dtype=np.byte)
#         A2[np.arange(n - 2), np.arange(n - 2)] = 1
#         A2[np.arange(n - 2), np.arange(2, n)] = -1
#         B2 = np.concatenate((-A2, A2), axis=1, )
#         B2 = np.concatenate((B2, -B2), axis=0, )
#
#         xij2 = (x[:-2] - x[2:])
#         b2 = np.concatenate((xij2 + max*2, -xij2 + min*2), axis=0)
#         #merge one and two
#
#         B = np.concatenate((B, B2), axis=0, )
#         b = np.concatenate((b,b2))

    A_ub = sp.coo_matrix(A_ub)

    # A_eq = None
    # b_eq = None
    # if labels is not None:
    #     labels = np.array(labels)
    #     A_eq = np.zeros((len(x),len(x)),dtype=np.int)
    #     A_eq[labels,labels] = 1
    #
    #     truth = np.array(truth)
    #     constr = np.concatenate( (abs(uuncost-truth)/2+(truth-uuncost)/2, abs(x-truth)/2-(truth-x)/2  ) )
    #
    #     b_eq = np.zeros_like(constr)
    #     b_eq[labels] = constr[labels]
    #     b_eq[labels+n] = constr[labels+n]
    #
    #
    #     D1 = np.concatenate((A_eq, np.zeros_like(A_eq)), axis=0, )
    #     D2 = np.concatenate((np.zeros_like(A_eq), A_eq), axis=0, )
    #     A_eq =  np.concatenate((D1,D2), axis=1, )

    #
    #print(sum(b_eq), "bew")
    A_eq = None
    b_eq = None
    # A_ub = None
    # b_ub = None
    solution = opt.linprog(c, A_ub=A_ub, b_ub=b_ub,A_eq=A_eq,b_eq=b_eq, bounds=(0, np.inf), options={"disp": False})
    uv = solution.x
    print(solution)
    print(uv , "labbeled")
    x_prime = x + uv[:int(len(uv) / 2)] - uv[int(len(uv) / 2):]

    return x_prime

# print(LPconstrainedAE(np.arange(500)))
# example form the paper
# x = np.array([12, 12.5, 13, 10, 15, 15.5])
# t = np.array([1, 2, 3, 5, 7, 8])
#
#




# start = timer()
# sol = LPconstrainedAE(np.arange(15000), 0.5, 0.5, time=np.arange(15000), w=1 )
# end = timer()
# print(end-start)
# print(sol, "thiiiis")
#
# paper = np.array([12, 12.5, 13, 14, 15, 15.5])


