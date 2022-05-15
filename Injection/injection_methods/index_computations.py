import math

import numpy as np

def get_random_indices(array_or_size,a_size = 1, number_of_ranges=1, percentage = None):
    size = array_or_size if isinstance(array_or_size,int) else len(array_or_size)

    if percentage is not None:
        print("percentage" , percentage, "asize" , a_size)
        number_of_ranges = math.ceil(size/100*percentage/a_size)

    free_space = size - number_of_ranges*a_size
    assert free_space >= 0 , f"not enough space for data size: {size} " \
                             f", number of ranges: {number_of_ranges} and range length:{a_size}"

    n_gaps = number_of_ranges + 1  # start , end , inbetween
    min_gap = int(free_space/5/n_gaps)

    random_space = free_space-min_gap*n_gaps

    print("r_gap",random_space)
    probabilities = np.random.uniform(size=n_gaps) # more variable outcomes
    probabilities = probabilities / sum(probabilities)
    random_spaces = np.random.multinomial(random_space , probabilities)
    spaces = random_spaces+min_gap

    assert sum(random_spaces) ==  random_space
    assert sum(spaces) == free_space , f" {sum(spaces) } != {free_space} "

    anom_ranges = [ np.arange(index+n*a_size,index+n*a_size+a_size)  for n ,index in enumerate(np.cumsum(spaces)[:-1])]

    assert len(anom_ranges) == number_of_ranges
    assert max(anom_ranges[-1]) < size
    return anom_ranges

x = np.arange(1000)



def get_free_spaces(arr):
    arr = np.ones_like(arr) - np.array(arr, dtype=bool)
    results = []
    current = []
    for index, value in enumerate(arr):
        if value:
            current.append(index)
        if not value:
            if len(current) == 0:
                pass
            else:
                results.append(np.array(current))
                current = []
    if len(current) > 0:
        results.append(np.array(current))

    return results
