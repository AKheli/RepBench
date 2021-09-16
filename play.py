

import timeit


if __name__ == '__main__':
    a = timeit.timeit( (lambda : 3*5+11*300))
    b = timeit.timeit( "3*5+11*300")
    print(a)
    print(b)

    x = (lambda : 3*5+11*300)
    a = timeit.timeit( x)
    print(a)

    def y(): return  3*5+11*300
    a = timeit.timeit(y)
    print(a)