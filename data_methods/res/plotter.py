# import matplotlib.pyplot as plt
# import numpy as np
# import scipy
# import pandas as pd
#
# #todo add labels to add so we can test imr with different labels
#
# class Plotter:
#
#     def get_indexes(self):
#         return  np.array(self.indexes)  if len(self.indexes) == len(self.injected) else np.arange(len(self.injected))
#
#     def __init__(self, injected=[], truth=[], labels=[], indexes=[], title=""):
#         self.truth = list(truth)
#         self.injected = injected
#         self.indexes = indexes
#         self.labels = labels
#         self.lines = {}
#         self.markers = ["s", "P", "+", "<", ">", "8", "p"]*10
#         self.colors = ["blue", "green", "yellow", "orange" ,"m" , "y", "tan"]
#         self.dots = [(3, 3), (3, 1), (3, 3, 1, 3), (3, 1, 1, 1), (3, 3, 1, 1, 3)]
#         self.title = title
#         self.color_map = {}
#
#     def add(self, values, name, type, color=None, lw=2):
#
#         if color is None:
#             if type not in self.color_map.keys():
#                 self.color_map[type] = self.colors.pop(0)
#             color = self.color_map[type]
#
#         d = sum(1 for x in self.lines.values() if x["type"] == type)
#         self.lines[name] = {"values": values, "type": type, "linestyle": (0, self.dots[d]), "color": color, "lw": lw}
#
#     def show(self):
#         self.get_plot().show()
#
#     def get_plot(self):
#         indexes = np.array(self.get_indexes())
#
#
#         if(len(self.labels) > 2):
#             plt.plot(indexes[self.labels], np.array(self.truth)[self.labels], 'o', mfc='none', label="labels",
#                      color="blue")
#
#         for key, value in self.lines.items():
#             ls = value["linestyle"]
#             color = value["color"]
#
#             plt.plot(indexes, value["values"], label=key, color=color,
#                      linestyle=ls) #marker=self.markers.pop(0), mfc='none')
#
#         plt.plot(indexes, self.injected, label="anomaly", color="red", ls=(0, (1, 1)))
#         plt.plot(indexes, self.truth, label="truth", color="black")
#         plt.title(self.title)
#
#         plt.legend()
#         return plt
#
#     def plotsats(self, eval=("rmse", "pearson")):
#         plt.subplots_adjust(bottom=0.35, top=0.92, right=0.82)
#         self.get_plot()
#
#         data = {}
#
#         values = list(self.lines.values())
#         algos = list(self.lines.keys())
#
#         data["algos"] = ["injected"] + algos
#         for i in eval:
#             if i[0] in ["r","R"]:
#                 data["rmse"] = [rms(self.truth, self.injected)] +  [rms(self.truth, d["values"]) for d in values ]
#
#             if i[0] in ["P", "p"]:
#                 data["pearson"] = [ round(a[0],4) for a in   [pearson(self.truth, self.injected)] +  [pearson(self.truth, d["values"]) for d in values] ]
#
#         lenghts = [max(x)*10 for x in  [[ len(str(entry)) for entry in v ]  for v in  data.values()]]
#         df = pd.DataFrame(data=data)
#         table = plt.table(bbox=(0.13, -0.6, 0.2 * len(data.keys()), 0.5), cellText=df.values, colLabels=df.columns, cellLoc="left",
#                   loc='center', colWidths=lenghts)
#
#
#
#         plt.legend() #mode="expand", bbox_to_anchor=(1.01, 0.5, 0.1, 0.5), loc='upper right', borderaxespad=0.)
#
#
#         return plt
#
#
# def rms(x, y, labels=[], r= 3):
#     x = np.array(x)
#     y = np.array(y)
#     labeled_x, labeled_y = x[labels], y[labels]
#     return round(np.sqrt(
#         (np.sum(np.square(x - y)) - np.sum(np.square(labeled_x - labeled_y)))
#         / (len(x) - len(labeled_x))
#     ),r)
#
#
# def pearson(x, y):
#     return scipy.stats.pearsonr(x, y)
