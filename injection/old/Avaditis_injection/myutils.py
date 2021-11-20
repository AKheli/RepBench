import pandas as pd
from pandas.tseries.frequencies import to_offset


#from utils

def _add(x, y):
    """
    Adds to values
    :param x: first value
    :param y: second value
    :return: result of the addition
    """

    return x + y

def _subtract(x, y):
    """
    Subtracts two values
    :param x: first value
    :param y: second value
    :return: result of the subtraction
    """

    return x - y


def next_dt(dt, f, inferred_freq, size=1):
    """
    Provides a later or earlier datetime from the given datetime that corresponds
    to a certain frequency and size.
    :param dt: a datetime object
    :param f: a function to either subtract or add two datetime object
    :param freq: the frequency for the timedelta
    :param size: the size of the window (that is applied with the frequency)
    :return: the next later or earlier datetime
    """

    # some freqs require relative offset, others can be computed with timedelta
    if inferred_freq.endswith(('MS', 'AS', 'B', 'W', 'M', 'SM', 'BM', 'CBM', 'SMS', 'BMS', 'CBMS', 'Q', 'BQ', 'QS', 'BQS', 'A', 'Y', 'BA', 'BY', 'YS', 'BAS', 'BYS', 'BH')):
        next_dt = (f(dt, to_offset(inferred_freq) * size)).to_pydatetime()
    else:
        next_dt = f(dt, pd.to_timedelta(to_offset(inferred_freq)) * size)

    return next_dt

def next_earlier_dt(dt, inferred_freq, size=1):
    return next_dt(dt, lambda x, y: _subtract(x,y), inferred_freq, size)


def next_later_dt(dt, inferred_freq, size=1):
    return next_dt(dt, lambda x, y: _add(x,y), inferred_freq, size)