import os

import pandas as pd
import numpy as np
import json
import IMR.IMR as IMR
from Screen.Local import screen

from PyPDF2 import PdfFileMerger


def rms(x,y,labels= [] , round = True):
    labeled_x , labeled_y = x[labels] , y[labels]
    return np.round(np.sqrt(
        (np.sum(np.square(x-y))- np.sum(np.square(labeled_x - labeled_y)))
        /(len(x)-len(labeled_x))
        ),4 )


dir  = "../data"
files = [dir+"/"+file for file in os.listdir(dir) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]


pdfs = []
folder = "/single" #/+2_amplitude_shifts"
for file in [dir+folder+"/"+file for file in os.listdir(dir+"/"+folder) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]:
    a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=0)
    with open(file + ".json") as f:
        data = json.load(f)
        print(data)

    #labels = [0, 1,2]  + [ anom["index_range"][0]  for anom in data.values()]+[ anom["index_range"][1]  for anom in data.values()]+[ anom["index_range"][2]  for anom in data.values()]
    #labels = np.concatenate((labels, np.random.randint(0, high=len(a["truth"]), size=15)), axis=None)
    labels = np.array([0, 1, 2, 5, 11])  # in the paper add +1

    y_0 = np.array(a["injected"]).copy()
    y_0[labels] = a["truth"][labels]


    plot1 = plotter(injected = a["injected"] , truth = a["truth"] , labels = labels , title = "test")


    #RMS= f'RMS original { rms(np.array(a["truth"]), np.array(a["injected"]))} \n'
    for p in [1,3]:
        a = a.copy()
        initial = y_0.copy()
        repair = IMR.imr2(a["injected"], y_0.copy(), labels, p=p, tau=0.1,k=2000)
        #assert sum(repair-IMR.imr(a["injected"], y_0.copy(), labels, p=p, tau=0.1,k=20000)) == 0
        plot1.add(values=repair, name=f"IMR({p})", type="imr")
        #RMS += f'RMS IMR({p}) = {rms(repair,np.array(a["truth"]),labels)} \n'

    s = 1
    repair_screen = screen(np.array([a["index"], a["injected"]]).T, T=1, SMIN=-s, SMAX=s)
    plot1.add( values =repair_screen , name = f"SCREEN({s})"  ,type = "screen")
    y_0 = np.array(a["injected"]).copy()
    y_0[labels] = a["truth"][labels]

    # repair_screen = screen(np.array([a["index"], y_0 ]).T, T=1, SMIN=-s, SMAX=s)
    # algos[f'SCREEN_l({s}) {rms(repair_screen, np.array(a["truth"]))}'] = repair_screen
    #RMS += f'RMS SCREEN({s})) = {rms(repair_screen, np.array(a["truth"]))}\n'

    plt = plot1.plotsats()

    if plt is not None:
        plt.savefig("pdfs/" +str(p)+ file.replace("/","") + ".pdf")
        plt.close()
        pdfs += ["pdfs/" +str(p)+ file.replace("/","") + ".pdf"]

        #IMR.IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))



#
#
# ### intel test data
#
#
# data = pd.read_csv("data/intel/ild3k.data",names = ["index","injected","y_0", "truth" , "label"],header = None)
#
# x = np.array(data["injected"])
# truth = np.array(data["truth"])
# labels = np.arange(len(x))[data["label"]]
# y_0 = np.array(data["y_0"])
#
# algos = {}
# for tau in [0.1,0.2]:
#     a = a.copy()
#     initial = y_0.copy()
#     repair = IMR.imr2(x , y_0.copy(), labels, p=3, tau=tau, k=20000)
#     algos[f'IMR(3,{tau}) {rms(repair, truth, labels)}'] = repair
#
#
#
# s = 1
# repair_screen = screen(np.array([data["index"], x.copy()]).T, T=1, SMIN=-s, SMAX=s)
# algos[f'SCREEN({s}) {rms(repair_screen, truth)}'] = repair_screen
#
# y_0 = x.copy()
# y_0[labels] =truth[labels]
#
# print(len(x))
# print(len(truth))
# plt = IMR.plot(x,algos, truth, "", labels, show=False,
#                observation_rms=" " + str(rms(x, truth)))
#
#
# if plt is not None:
#     plt.savefig("pdfs/" +" "+ ".pdf")
#     plt.close()
#     pdfs += ["pdfs/" + " " + ".pdf"]
#
# print("original rms" , rms(y_0,truth, labels))
# print("rms" , rms(repair,truth, labels))
#
#
# result = IMR.imr2(x,y_0,labels,tau=0.2,p=3)
# print("rms" , rms(result,truth, labels))
#
# result = IMR.imr2(x,y_0,labels,tau=0.2,p=1)
# print("rms" , rms(result,truth, labels))
#
# labels2 = np.arange(500)[data["label"][1500:2000]]
# #plt = IMR.plot(x[1500:2000],result[1500:2000],truth[1500:2000],labels = labels,index= np.arange(1500,2000), show = False)
#
# plt = IMR.plot(x,algos, truth, "intel lab example ", labels2, show=False,
#                observation_rms=" " + str(rms(x, truth)))
#
# if plt is not None:
#     plt.xlim([1500,2000])
#     plt.savefig("pdfs/" +" 1"+ ".pdf")
#     plt.close()
#     pdfs += ["pdfs/" + " 1" + ".pdf"]
#
#
# result = IMR.imr2(x.copy(),y_0,labels,tau=0.1,p=3,k=20000)
# print("normal rms" , rms(result,truth, labels))
#
# min
# for i in range(10):
#     labels = np.array([0,1,2]+list(np.random.randint(3,len(x),len(labels)-50)))
#     print(len(labels))
#     y_0 = x.copy()
#     y_0[labels] = truth[labels]
#     print(("rms" , rms(IMR.imr2(x.copy(),y_0,labels,tau=0.1,p=3,k=20000),truth, labels)))
#
#
#
#
# folder = "/extremestock" #/+2_amplitude_shifts"
# for file in [dir+folder+"/"+file for file in os.listdir(dir+"/"+folder) if file[-4:] != "json" and not os.path.isdir(dir+"/"+file)]:
#     a = pd.read_csv(file, names=["index", "truth", "injected", "class"], header=0)
#
#     with open(file.split(".")[0] + ".json") as f:
#         data = json.load(f)
#         print(data)
#
#     labels = [0, 1,2]  #+[ anom["index_range"][0]  for anom in data.values()]+[ anom["index_range"][1]  for anom in data.values()]+[ anom["index_range"][2]  for anom in data.values()]
#     labels = np.concatenate((labels, np.random.randint(0, high=len(a["truth"]), size= int(len(a["index"])/5))), axis=None)
#     #labels = np.array([0, 1, 2, 5, 11])  # in the paper add +1
#
#     y_0 = np.array(a["injected"]).copy()
#     y_0[labels] = a["truth"][labels]
#
#     algos = {}
#     #RMS= f'RMS original { rms(np.array(a["truth"]), np.array(a["injected"]))} \n'
#     for p in [1,3]:
#         a = a.copy()
#         initial = y_0.copy()
#         repair = IMR.imr2(a["injected"], y_0.copy(), labels, p=p, tau=0.1,k=2000)
#         #assert sum(repair-IMR.imr(a["injected"], y_0.copy(), labels, p=p, tau=0.1,k=20000)) == 0
#         algos[f'IMR({p}) {rms(repair,np.array(a["truth"]),labels)}'] = repair
#         #RMS += f'RMS IMR({p}) = {rms(repair,np.array(a["truth"]),labels)} \n'
#
#     s = 2
#     repair_screen = screen(np.array([a["index"], a["injected"]]).T, T=6, SMIN=-s, SMAX=s)
#     algos[f'SCREEN({s}) {rms(repair_screen, np.array(a["truth"]))}'] = repair_screen
#
#     y_0 = np.array(a["injected"]).copy()
#     y_0[labels] = a["truth"][labels]
#
#     # repair_screen = screen(np.array([a["index"], y_0 ]).T, T=1, SMIN=-s, SMAX=s)
#     # algos[f'SCREEN_l({s}) {rms(repair_screen, np.array(a["truth"]))}'] = repair_screen
#     #RMS += f'RMS SCREEN({s})) = {rms(repair_screen, np.array(a["truth"]))}\n'
#
#     plt = IMR.plot(a["injected"],algos,a["truth"], file.split("/")[-1] ,labels,show=False,observation_rms=" " + str(rms(np.array(a["injected"]),np.array(a["truth"]))))
#     plt  = plotter(injected=a["injected"] , )
#     if plt is not None:
#         name = random.randint(0,100000)
#         plt.savefig("pdfs/" +str(name)+ file.replace("/","") + ".pdf")
#         plt.close()
#         pdfs += ["pdfs/" +str(name)+ file.replace("/","") + ".pdf"]
#
#         #IMR.IMRsave(a["index"],a["injected"],y_0,a["truth"],labels ,y_k,"p"+str(3)+file.replace(dir+"/",""))

merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write( f'test')
merger.close()


def delete():
    try:
        for pdf in pdfs:
            os.remove(pdf)
    except:
        pass
        #delete()
delete()
