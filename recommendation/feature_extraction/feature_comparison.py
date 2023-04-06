import numpy as np
import pandas as pd
import pycatch22

from injection import inject_data_df
from injection.injection_config import *
import matplotlib.pyplot as plt


def catch_22_features(df):
    context = {}
    ### catch22 features
    import pycatch22
    context["catch22"] = {}

    features_min_max = {}  # name: {min: min_val , max: max_val}
    for i, ts in enumerate(df.columns):
        ts_data = df[ts].values
        features = pycatch22.catch22_all(ts_data)
        if i == 0:
            features_min_max = {name: {} for name in features["names"]}
        features = {name: round(val, 4) for name, val in zip(features["names"], features["values"])}
        if i == 0:
            features_min_max = {name: {"min": val, "max": val} for name, val in features.items()}
        for name, val in features.items():
            if val < features_min_max[name].get("min"):
                features_min_max[name]["min"] = val
            if val > features_min_max[name].get("max"):
                features_min_max[name]["max"] = val
        context["catch22"][ts] = features
    for i, ts in enumerate(df.columns):
        for name, val in context["catch22"][ts].items():
            context["catch22"][ts][name] = {"value": val, "min": features_min_max[name]["min"],
                                            "max": features_min_max[name]["max"]}

    context["catch22_min_max"] = features_min_max
    return context



datasets =  ["bafu5k", "humidity" , "elec"]
a_types = [AMPLITUDE_SHIFT, POINT_OUTLIER, DISTORTION]
column = 0

# create plot with all datasets and all anomaly types

fig, axs = plt.subplots(len(datasets), len(a_types), figsize=(20,20))
for d_i , dataset in enumerate(datasets):
    for a_i , a_type in enumerate(a_types):
        ax = axs[d_i, a_i]

        truth_df = pd.read_csv(f"data/test/{dataset}.csv")
        ts_data_true = truth_df.iloc[:, column].values
        true_features  = pycatch22.catch22_all(ts_data_true)
        plt.plot(true_features["values"], label="true")

        # plt.plot(true_features["values"], label="true")

        for factor in [1,2,3,5,10]:
            injected_df, _ = inject_data_df(truth_df, a_type=a_type , cols=[column], factor=factor)
            ts_data_injected = injected_df.iloc[:, column].values
            injected_features = pycatch22.catch22_all(ts_data_injected)
            injected_features["values"] = [x for i,x in enumerate(injected_features["values"])]
            ax.plot(injected_features["values"], linestyle="--",label=f"factor={factor}")

        ax.set_xticks(range(len(true_features["names"])), [x[:5]  for x in true_features["names"] if len(x) > 6] , rotation=90)
        ax.set_title(f"{dataset} {a_type}")
        ax.legend()

fig.text(0.5, 0.04, 'Anomaly Type', ha='center' , size=25)
fig.text(0.04, 0.5, 'Dataset', va='center', rotation='vertical',size=25)
fig.text(0.5, 0.95, 'Features', ha='center', size=25)

fig.subplots_adjust(hspace=0.2)
fig.savefig(f"features_plot.png")

fig, axs = plt.subplots(len(datasets), len(a_types), figsize=(20,20))
for d_i , dataset in enumerate(datasets):
    for a_i , a_type in enumerate(a_types):
        ax = axs[d_i, a_i]

        truth_df = pd.read_csv(f"data/test/{dataset}.csv")
        ts_data_true = truth_df.iloc[:, column].values
        true_features  = pycatch22.catch22_all(ts_data_true)


        # plt.plot(true_features["values"], label="true")

        for factor in [1,2,3,5,10]:
            injected_df, _ = inject_data_df(truth_df, a_type=a_type , cols=[column], factor=factor)
            ts_data_injected = injected_df.iloc[:, column].values
            injected_features = pycatch22.catch22_all(ts_data_injected)
            injected_features["values"] = [x/true_features["values"][i] for i,x in enumerate(injected_features["values"])]
            ax.plot(injected_features["values"], linestyle="--",label=f"factor={factor}")

        ax.set_xticks(range(len(true_features["names"])), [x[:5]  for x in true_features["names"] if len(x) > 6] , rotation=90)
        ax.set_title(f"{dataset} {a_type}")
        ax.legend()

fig.text(0.5, 0.04, 'Anomaly Type', ha='center' , size=25)
fig.text(0.04, 0.5, 'Dataset', va='center', rotation='vertical',size=25)
## add title
fig.text(0.5, 0.95, 'Features divided by the feature value of the True Series', ha='center', size=25)
fig.subplots_adjust(hspace=0.2)
fig.savefig(f"features_divided_by_true_plot.png")


