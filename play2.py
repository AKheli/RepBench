from abc import abstractmethod

from matplotlib import pyplot as plt



import time


def time_it(f):
    def wrapper(b, *args):
        t = time.time()
        result = f(b, *args)
        b._time = time.time() - t
        return result

    return wrapper

class B:
    def __init__(self):
        self._time = 0