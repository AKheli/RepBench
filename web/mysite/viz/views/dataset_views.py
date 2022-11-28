import os

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from pandas import DataFrame

from data_methods.data_class import DataContainer
from web.mysite.viz.ts_manager.ts_manager import get_truth_data

## match case for dataset
data_set_map = {"bafu5k": "BAFU",
                "msd1_5": "Server Maschine Dataset",
                "humidity": "Humidity",
                "small": "Small",
                "elec": "Electricity",
                "tiny" : "Tiny",
                "20" : "20",
                }


# data_set_description_map = {"bafu5k": "The BAFU dataset contains 5k time series with 1000 values each. The time series are sampled at 1 minute intervals. The values are the temperature in degrees Celsius.",
#                             "msd1_5": "The Server Maschine Dataset contains 1.5k time series with 1000 values each. The time series are sampled at 1 minute intervals. The values are the temperature in degrees Celsius.",
#                             "humidity": "The Humidity dataset contains 1k time series with 1000 values each. The time series are sampled at 1 minute intervals. The values are the humidity in percent.",
#

data_set_shape_map = {key: pd.read_csv(f"data/train/{key}.csv").shape for key in data_set_map.keys()}

class DatasetView(View):
    default_nbr_of_ts_to_display = 5

    def load_data_set(self,setname):
        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
        return df

    def data_set_info_context(self, df,setname):
        correlation_html = df.corr().round(3).to_html(classes=["table table-sm table-dark"],table_id='correlation_table')
        context = {"correlation_html" : correlation_html}
        return context

    def data_set_default_context(self, request,setname):
        df = self.load_data_set(setname)
        context = {"setname": setname}
        context["data_title"] = data_set_map.get(setname, setname)
        context["viz"] = int(request.GET.get("viz", self.default_nbr_of_ts_to_display))
        return context , df


    def get(self,request,setname = "bafu5k"):
        context, df = self.data_set_default_context(request,setname)
        context.update(self.data_set_info_context(df,setname))
        print(context)
        return render(request, 'displayDataset.html', context=context)


    def get_data(self ,request, setname="bafu5k"):
        viz = int(request.GET.get("viz", 5))
        return JsonResponse(get_truth_data(setname, viz=viz))




### display_datasets.html page
def mult_tup(tup):
    return tup[0] * tup[1]


def display_datasets(request=None):
    data_files = [f.split(".")[0] for f in os.listdir("data/train")]
    context = {"datasets": {data_set_map.get(f, f):
                                {"full_file_name": f.split(".")[0],
                                 "ts_nbr": data_set_shape_map[f][1],
                                 "values": mult_tup(data_set_shape_map[f])}

                            for f in data_files}}

    return render(request, 'displayDatasets.html', context=context)


