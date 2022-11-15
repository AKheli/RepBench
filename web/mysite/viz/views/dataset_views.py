import os

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from pandas import DataFrame

## match case for dataset
data_set_map = {"bafu5k": "BAFU",
                "msd1_5": "Server Maschine Dataset",
                "humidity": "Humidity",
                "small": "Test",
                "elec": "Electricity",
                }

data_set_shape_map = {key: pd.read_csv(f"data/train/{key}.csv").shape for key in data_set_map.keys()}

class DatasetView(View):
    default_nbr_of_ts_to_display = 5


    def load_data_set(self,setname):
        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
        return df

    def data_set_info_context(self, df):
        correlation_html = df.corr().round(3).to_html(classes=["table table-sm table-dark"])
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
        context.update(self.data_set_info_context(df))
        print(context)
        return render(request, 'displayDataset.html', context=context)


    def get_data(self ,request, setname="bafu5k"):
        df = self.load_data_set(setname)
        viz = int(request.GET.get("viz", 5))

        data = {
            'series': [{"visible": i < viz, "id": col_name, "name": col_name, "data": list(df[col_name])} for (i, col_name)
                       in
                       enumerate(df.columns)],
        }
        return JsonResponse(data)




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


