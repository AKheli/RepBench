import json
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.views import View

from WebApp.viz.views import data_loader
import WebApp.viz.datasetsConfig as datasetsConfig
from WebApp.viz.models import DataSet, InjectedContainer


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return round(float(obj), 3)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, float):
            return round(obj, 3)
        return json.JSONEncoder.default(self, obj)


class DatasetView(View):
    default_nbr_of_ts_to_display = 5
    template = 'displayDataset.html'
    encoder = NpEncoder
    data_fetch_url_name = "get_data"
    load_data_container = data_loader.load_data_container

    def data_set_info_context(self, setname):
        dataSet = DataSet.objects.get(title=setname)
        df = dataSet.df
        corr = df.corr().round(3)
        correlation_html = df.corr().round(3).to_html(classes=["table table-sm table-dark"],
                                                      table_id='correlation_table')
        corr_data = []
        for i, row in enumerate(corr.values):
            for j, v in enumerate(row):
                corr_data.append([i, j, v])
        columns = df.columns.tolist()

        context = {"correlation_html": correlation_html}

        context["data_info"] = dataSet.get_info()
        context["columns"] = columns
        context["corr_data"] = corr_data

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
        catch22_df = pd.DataFrame.from_dict(context["catch22"])
        catch22_df.columns.name = 'catch22 feature'
        context["catch22_html"] = catch22_df.to_html(classes=["table table-sm table-dark"],
                                                     table_id='catch_22_table', index=True)

        return context

    def data_set_default_context(self, request, setname=datasetsConfig.default_set):
        data_container = data_loader.load_data_container(setname)
        df = data_container.original_data
        context = {"setname": setname}
        context["viz"] = int(request.GET.get("viz", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        return context, df

    def get(self, request, setname=datasetsConfig.default_set):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_info_context(setname))
        print(context)
        return render(request, self.template, context=context)



def display_datasets(request=None):
    context = {"datasets": {dataSet.title: dataSet.get_info()
                            for dataSet in DataSet.objects.all()}}

    context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
                                    for dataSet in InjectedContainer.objects.all() if dataSet.title is not None and dataSet.title != ""}
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print( context["syntheticDatasets"])
    return render(request, 'displayDatasets.html', context=context)
