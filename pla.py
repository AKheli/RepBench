import matplotlib.pyplot as plt
from matplotlib.legend import Legend
import numpy as np
import pandas as pd
import time

#f, axs = plt.subplots()
colors  = list()

lines = []
labels = []
for i in range(10):
    p = plt.plot(range(100), [x + i*10 for x in range(100)],linestyle = (0, (i*2+1, 1)),label = i)
    colors.append(p[-1].get_color())
    lines += p
    labels.append(i)
# axs[0].legend(bbox_to_anchor=(0., -0.25, 1., 0.00), loc='lower left',
#                    ncol=3, mode="expand", borderaxespad=0.)
print(colors)
lines = lines[:4]
plt.subplots_adjust(bottom=0.35, top = 0.92 ,right = 0.82)
df = pd.DataFrame(data = {"rmse": [1]*len(lines), "irgend": [1]*len(lines)})
the_table = plt.table(bbox= (0.13,-0.6,0.4,0.5) ,cellText=df.values,colLabels=df.columns,cellLoc = "left",loc='center', colWidths=[0.1,0.1],colColours = colors[:4])
plt.legend(mode="expand",bbox_to_anchor=(1.01,0.5,0.1,0.5), loc='upper right',                 borderaxespad=0.)
#leg = Legend(axs[1], lines,labels, frameon=False,bbox_transform=(2, -100000000000, 1., 1))
#axs.add_artist(leg)
plt.show()



# import Paper1.IMR as IMR
#
#
# start = time.time()
# data = pd.read_csv("evaluation/data/intel/ild3k.data",names = ["index","injected","y_0", "truth" , "label"],header = None)
#
# x = np.array(data["injected"])
# truth = np.array(data["truth"])
# labels = np.arange(len(x))[data["label"]]
# y_0 = np.array(data["y_0"])
#
# algos = {}
#
# for i in range(100):
#     data = data.copy()
#     initial = y_0.copy()
#     repair = IMR.imr2(x , y_0.copy(), labels, p=3, tau=0.1, k=10000)
#     #algos[f'IMR(3,{tau}) {rms(repair, truth, labels)}'] = repair
#
# end = time.time()
# print(end - start)
