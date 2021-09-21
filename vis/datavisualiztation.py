from Screen.Local import screen
import pandas
import matplotlib.pyplot as plt

datafile = "..\stock10k.datasets"


Series = (pandas.read_csv(datafile, names=("timestamp", "mod", "true"))).to_numpy()


repair = screen(Series)
d = Series[:,1]
truth = Series[:,2]

print(repair[d!=truth])







plt.plot(Series[:,0], Series[:,1:] )
plt.show()

plt.plot(repair ,color = 'r')
plt.show()

# plt.plot(Series[:,0], screen(Series)   )
# plt.show()



