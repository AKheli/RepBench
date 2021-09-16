from main import screen
import pandas
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer


datafile = "stock10k.data"

RMS = lambda x, y: np.mean(np.square(x - y)) ** (1 / 2)
Series = (pandas.read_csv(datafile, names=("timestamp", "mod", "true"))).to_numpy()
truth = Series[:,2]*1
dirty = Series[:,1]*1
repair = screen(Series)

def accuracy(truth,dirty):
    def a(repair):
        return 1-RMS(truth[:len(repair)],repair)/(RMS(repair,dirty[:len(repair)])+RMS(truth[:len(repair)],dirty[:len(repair)]))
    return a
acc = accuracy(truth,dirty)

print(acc(repair))


def measuretime(function,input):
    start = timer()
    function(*input)
    end = timer()
    return end - start



results = [ acc(screen(Series,a)) for a in (np.arange(stop = 13,start=1)*1000)]
print(np.arange(stop = 13,start=1)*1000)

plt.plot(results,alpha=0.8)
plt.axis([0, 11, 0, 1] )
plt.show()



