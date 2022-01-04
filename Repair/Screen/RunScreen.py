from Repair.Screen.Local import screen
import pandas
import numpy as np
import matplotlib.pyplot as plt
from Repair.Screen.GlobalLP import LPconstrainedAE
from modelevaluation.comparingPlots import visualize
from modelevaluation.seriesAnalysis import biggestdifference



datafile = "../datasets/stock/stock10k.Data"

def RMS( x, y): return np.mean(np.square(x - y[:len(x)])) ** (1 / 2)

def accuracy(truth,dirty):
    def a(repair):
        return 1-RMS(truth[:len(repair)],repair)/(RMS(repair,dirty[:len(repair)])+RMS(truth[:len(repair)],dirty[:len(repair)]))
    return a



def visualizeLocaLvsGlobal(datafile = datafile, evelfunction = RMS):
    Series = (pandas.read_csv(datafile, names=("timestamp", "mod", "true"))).to_numpy()
    truth = Series[:,2]*1
    dirty = Series[:, 1]*1
    dirty_copy = np.copy(dirty)
    repair = screen(Series)

    acc = accuracy(truth, dirty)

    evalfun = lambda x : evelfunction(x,truth)
    f_name = "functionname"

    results = [ evalfun(screen(Series,a)) for a in (np.arange(stop = 14,start=1)*1000)]
    print(np.arange(stop = 13,start=1)*1000)
    print(results)
    plt.plot(results ,color = 'blue')


    results = [ evalfun(LPconstrainedAE( np.copy(dirty_copy[:a]))) for a in (np.arange(stop = 14,start=1)*1000)]
    plt.plot(results ,color = 'black')
    print(results)

    #Results = [ evalfun(  LPconstrainedAE(np.copy(dirty_copy[:a]), second = True)) for a in (np.arange(stop = 14,start=1)*1000)]
    #plt.plot(Results ,color = 'g')


    plt.axis([0, 12, 0, 5] )
    plt.savefig(f_name)
    plt.show()

    lp = LPconstrainedAE(dirty*1)
    np.savetxt("result2.csv", lp*1, delimiter=",")
    print(lp*1)
    print(RMS(truth*1,lp*1))
    print(RMS(truth*1,dirty*1))
    print(RMS(truth*1,repair*1))

#visualizeLocaLvsGlobal()

Series = (pandas.read_csv(datafile, names=("timestamp", "mod", "true"))).to_numpy()
truth = Series[:, 2] * 1
dirty = Series[:, 1] * 1
dirty = np.copy(dirty)

lp = LPconstrainedAE(dirty)
sc = screen(Series)

visualize(dirty,lp,truth)
visualize(dirty,sc,truth)

print(biggestdifference(lp,truth))
print(biggestdifference(sc,truth))
print(biggestdifference(dirty,truth))

a = biggestdifference(lp,truth)
visualize(dirty,lp,truth, section=(a-10,a+10))
visualize(dirty,sc,truth, section=(a-10,a+10))

a = biggestdifference(sc,truth)
visualize(dirty,lp,truth, section=(a-10,a+10) ,title="lp")
visualize(dirty,sc,truth, section=(a-20,a+20), title="sc")









