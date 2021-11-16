import os

import pandas as pd
import numpy as np
import json
from repair_algos.IMR import IMR as IMR
from repair_algos.Screen.Local import screen
from res.file_manipulation import files_from_comma_string
from res.plot_to_pdf import PDFsaver

saver = PDFsaver("IMRscript")
dir  = "Data/Injected_data/"

files = files_from_comma_string(dir+"2_amplitude_shifts")

for file in files:
    a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=0)
    with open(file + ".json") as f:
        data = json.load(f)
        print(data)

    labels = [0, 1,2]  #+ [ anom["index_range"][0]  for anom in Data.values()]+[ anom["index_range"][1]  for anom in Data.values()]+[ anom["index_range"][2]  for anom in Data.values()]
    labels = np.concatenate((labels, np.random.randint(0, high=len(a["truth"]), size=20)), axis=None)
    #labels = [0, 1, 2, 5, 11]  # in the paper add +1

    y_0 = np.array(a["injected"]).copy()
    y_0[labels] = a["truth"][labels]

    algos = {}
    for p in [1,3]:
        a = a.copy()
        initial = y_0.copy()
        repair = IMR.imr2(a["injected"], y_0.copy(), labels, p=p, tau=0.1, k=200000)
        algos[f'IMR({p})         {rms(repair,np.array(a["truth"]),labels)}'] = repair

    s = 1
    repair_screen = screen(np.array([a["index"], a["injected"]]).T, T=1, SMIN=-s, SMAX=s)
    algos[f'SCREEN({s})    {rms(repair_screen, np.array(a["truth"]))}'] = repair_screen

    y_0 = np.array(a["injected"]).copy()
    y_0[labels] = a["truth"][labels]

    # repair_screen = screen(np.array([a["index"], y_0 ]).T, T=1, SMIN=-s, SMAX=s)
    # algos[f'SCREEN_l({s}) {rms(repair_screen, np.array(a["truth"]))}'] = repair_screen
    #RMS += f'RMS SCREEN({s})) = {rms(repair_screen, np.array(a["truth"]))}\n'

    plt = IMR.plot(a["injected"], algos, a["truth"], " ", labels, show=False, observation_rms=" " + str(rms(np.array(a["injected"]), np.array(a["truth"]))))

    if plt is not None:
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=3, mode="expand", borderaxespad=0.)
        plt.subplots_adjust(top= 0.83,bottom=0.08)
        plt.savefig("tmp/" +str(p)+ file.replace("/","") + ".pdf")
        plt.close()
        saver.add(plt)
        #IMR.IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))

print(saver.pdfs)
saver.close()




