import os

import pandas as pd
import numpy as np
from Repair.repair_algos.IMR import IMR as IMR
from Repair.repair_algos.Screen.Local import screen

from PyPDF2 import PdfFileMerger

dir  = "../../Data"
files = [dir+"/"+file for file in os.listdir(dir) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]


pdfs = []
folder = "amplitude_shift"
T = 1
for file in [dir+"/"+folder+"/"+file for file in os.listdir(dir+"/"+folder) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]:
    for s in [0.2,1,3]:
        a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=0)

        repair_screen = screen(np.array([a["index"], a["injected"]]).T, T=2, SMIN=-s, SMAX=s)

        plt = IMR.plot(a["injected"], repair_screen, a["truth"], file.replace("/", " ") + " s=" + str(s), show=False)

        if plt is not None:
            plt.savefig("tmp/" +str(s)+ file.replace("/","") + ".pdf")
            plt.close()
            pdfs += ["tmp/" +str(s)+ file.replace("/","") + ".pdf"]

        #IMR.IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))


merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write( f'{folder}_SCREEN_t={T}.pdf')
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

##notes
#imr highly depends on where the labels are placed