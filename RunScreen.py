from main import screen
import pandas
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from other_models.LP import LPconstrainedAE


datafile = "stock10k.data"

def RMS( x, y): return np.mean(np.square(x - y[:len(x)])) ** (1 / 2)

def accuracy(truth,dirty):
    def a(repair):
        return 1-RMS(truth[:len(repair)],repair)/(RMS(repair,dirty[:len(repair)])+RMS(truth[:len(repair)],dirty[:len(repair)]))
    return a


Series = (pandas.read_csv(datafile, names=("timestamp", "mod", "true"))).to_numpy()
truth = Series[:,2]*1
dirty = Series[:, 1]*1
dirty_copy = np.copy(dirty)
repair = screen(Series)



acc = accuracy(truth,dirty)

print(acc(repair))


def measuretime(function,input):
    start = timer()
    function(*input)
    end = timer()
    return end - start




evalfun , f_name =  lambda x : RMS(x,truth) , "RMS" # acc , "acc66"


results = [ evalfun(screen(Series,a)) for a in (np.arange(stop = 14,start=1)*1000)]
print(np.arange(stop = 13,start=1)*1000)
plt.plot(results ,color = 'blue')


results = [ evalfun(LPconstrainedAE( np.copy(dirty_copy[:a]))) for a in (np.arange(stop = 14,start=1)*1000)]
plt.plot(results ,color = 'black')

#results = [ evalfun(  LPconstrainedAE(np.copy(dirty_copy[:a]), second = True)) for a in (np.arange(stop = 14,start=1)*1000)]
#plt.plot(results ,color = 'g')


plt.axis([0, 12, 0, 5] )
plt.savefig(f_name)
plt.show()

lp = LPconstrainedAE(dirty*1)
np.savetxt("result2.csv", lp*1, delimiter=",")
print(lp*1)
print(RMS(truth*1,lp*1))
print(RMS(truth*1,dirty*1))
print(RMS(truth*1,repair*1))





