import os
from errno import EACCES

import pandas as pd
import numpy as np
import json
import Paper1.IMR as IMR
from Screen.Local import screen
import matplotlib.pyplot as plt

from PyPDF2 import PdfFileMerger






dir  = "data"
files = [dir+"/"+file for file in os.listdir(dir) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]


#for file in files:
    # for i in range(5):
    #     a = pd.read_csv(file , names = ["index","truth","injected","class"] ,header  = 1)
    #     repair_screen = screen(np.array([a["index"], a["injected"]]).T,T=i, SMIN=-0.5,SMAX=0.5)
    #     plt.plot(a["index"],a["injected"],label = "injected")
    #     plt.title("screen T="+str(i))
    #     plt.plot(a["index"],a["truth"],label = "truth")
    #     plt.plot(a["index"],repair_screen,label = "repair")
    #     plt.show()

# fig = plt.figure()
# for i, file in enumerate(files):
#     a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=1)
#     labels = np.random.randint(0, high=len(a["truth"]), size=15)
#     labels = np.concatenate((labels, [0,1,2]), axis=None)
#     y_0 = np.array(a["injected"])
#     print(file)
#     y_0[labels] = a["truth"][labels]
#     y_k = IMR(a["injected"],   y_0 ,labels ,p = 1)
#
#     plt.plot(a["index"], a["injected"],'x', label="injected")
#     #axis.title = "IMR"
#     plt.plot(a["index"],a["truth"], label = "truth")
#     plt.plot(a["index"],y_k,'o',label = "repair")
#     plt.plot(a["index"][labels],a["truth"][labels],'o',label = "labels", )
#     plt.legend()
#     plt.savefig("pdfs"+file[4:] +".pdf")
#     plt.close()

#     IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))

pdfs = []
for file in files:
    print(file)
    with open(file+".json") as f:
        data = json.load(f)
        print(data)

    a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=0)
    labels = [ anom["index_range"][0]  for anom in data.values()]+[ anom["index_range"][1]  for anom in data.values()]+[ anom["index_range"][2]  for anom in data.values()]
    labels = np.concatenate((labels, [0,1,2],np.random.randint(0, high=len(a["truth"]), size=15)), axis=None)
    y_0 = np.array(a["injected"]).copy()
    y_0[labels] = a["truth"][labels]
    y_k = IMR.imr(a["injected"],   y_0.copy() ,labels ,p = 3 , tau = 0.1)


    plt = IMR.plot(a["injected"],y_k,a["truth"],labels,file.replace("data/","") ,show=False)

    if plt is not None:
        plt.savefig("pdfs/" + file.replace("data/","") + ".pdf")
        plt.close()
        pdfs += ["pdfs/" + file.replace("data/","") + ".pdf"]

    #IMR.IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))


merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write("resultss.pdf")
merger.close()


def delete(i):
    try:
        for pdf in pdfs:
            print(pdf)
            os.remove(pdf)
    except PermissionError:
        print(i)
        delete(i+1)
delete(1)
