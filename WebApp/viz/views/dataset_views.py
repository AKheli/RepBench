import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from data_methods.data_class import DataContainer

import WebApp.viz.datasetsConfig as datasetsConfig
from WebApp.viz.ts_manager.HighchartsMapper import map_truth_data


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

    @staticmethod
    def load_data_container(setname):
        path = datasetsConfig.data_sets_info.get(setname).get("path")
        return DataContainer(path)

    def data_set_info_context(self, df, setname):
        correlation_html = df.corr().round(3).to_html(classes=["table table-sm table-dark"],
                                                      table_id='correlation_table')
        context = {"correlation_html": correlation_html}
        info = datasetsConfig.data_sets_info[setname]
        path = info["path"]
        n, m = pd.read_csv(f"data/{path}").shape
        info["values"] = n * m
        info["ts_nbr"] = m
        context["data_info"] = info
        return context

    def data_set_default_context(self, request, setname=datasetsConfig.default_set):
        data_container = self.load_data_container(setname)
        df = data_container.original_data
        context = {"setname": setname}
        context["data_title"] = datasetsConfig.data_sets_info.get(setname).get("title", setname)
        context["viz"] = int(request.GET.get("viz", self.default_nbr_of_ts_to_display))
        return context, df

    def get(self, request, setname=datasetsConfig.default_set):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_info_context(df, setname))
        return render(request, self.template, context=context)

    def get_data(self, request, setname=datasetsConfig.default_set):
        viz = int(request.GET.get("viz", 5))
        container = self.load_data_container(setname)
        return JsonResponse(map_truth_data(container, viz=viz))


def display_datasets(request=None):
    data_sets_info = datasetsConfig.data_sets_info
    for dataset, data_dict in data_sets_info.items():
        path = data_dict["path"]
        n, m = pd.read_csv(f"data/{path}").shape
        data_dict["values"] = n * m
        data_dict["ts_nbr"] = m

    context = {"datasets": data_sets_info}

    return render(request, 'displayDatasets.html', context=context)
