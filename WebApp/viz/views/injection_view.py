import json
import random

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

from injection.injected_data_container import InjectedDataContainer
from WebApp.viz.forms.alg_param_forms import SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField
from WebApp.viz.forms.injection_form import store_injection_form, InjectionForm
from WebApp.viz.models import InjectedContainer, DataSet
from injection.injection_methods.basic_injections import add_anomalies
from WebApp.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from WebApp.viz.ts_manager.HighchartsMapper import map_injected_series
from WebApp.viz.views.data_loader import load_data_container
from WebApp.viz.views.repair_view import RepairView
from testing_frame_work.data_methods.data_class import DataContainer


class InjectionView(RepairView):
    template = "injection.html"
    error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_rmse": "RMSE on Anomaly",
                 "runtime": "runtime"}

    ParamForms = {"SCREEN": SCREENparamForm(), "RPCA": RPCAparamForm(), "CDrec": CDparamForm(), "IMR": IMRparamField()}

    def get(self, request, setname="BAFU"):
        data_object = DataSet.objects.get(title=setname)
        df = data_object.df
        context = {"setname": setname}
        context["viz"] = int(request.GET.get("viz", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        context["store_form"] = store_injection_form
        context["injection_form"] = InjectionForm(list(df.columns))
        context["alg_forms"] = self.ParamForms

        return render(request, self.template, context=context)


def inject_data(request, setname):
    post = request.POST
    col_name = post.get("data_columns")

    data_object = DataSet.objects.get(title=setname)
    df = data_object.df
    title = data_object.title
    data_container =  DataContainer(df, title=title)

    df = data_container.norm_data
    if isinstance(df.columns, pd.Int64Index):
        col_name = int(col_name)

    col_norm = df[col_name]
    original_col = data_container.original_data[col_name]

    # anomaly injection values
    factor = float(post.get("factor"))
    ratio = float(post.get("ratio"))
    a_type = post.get("anomaly")
    seed = post.get("seed")

    if seed == '':
        seed = random.randint(0, 100)
    else:
        seed = int(seed)

    if a_type != "outlier":
        n_anomalies = int(ratio * df.shape[0] / 30) + 1
    else:
        n_anomalies = int(ratio * df.shape[0])

    col_injected_norm, _ = add_anomalies(col_norm,
                                    a_type=a_type,
                                    a_factor=factor,
                                    a_len=30,
                                    n_anomalies=n_anomalies,
                                    fill_na=True, seed=seed)
    col_injected = col_injected_norm * original_col.std() + original_col.mean()
    injected_series = map_injected_series(col_injected,col_injected_norm,col_name)
    return JsonResponse({"injected_series": injected_series})


def store_data(request, setname):
    post = request.POST.dict()
    title , min , max = post.get("title") , int(float(post.get("min"))) , int(float(post.get("max")))
    description = post.get("description")
    post.pop("csrfmiddlewaretoken")
    data_container = load_data_container(setname)
    df_norm = data_container.norm_data  # only work with normalized data
    df_original = data_container.original_data
    #df_original = data_container.original_data
    injected_series = json.loads(post.pop("injected_series"))

    df_norm = df_norm.iloc[min:max]

    for series_dict in injected_series:
        series_dict["data"] = series_dict["data"][min:max]

    injected_data_container : InjectedDataContainer = injected_container_None_Series(df_norm, injected_series)
    injected_data_container.set_to_original_scale(df_original.mean(), df_original.std())

    if InjectedContainer.objects.filter(title=title).exists():
        InjectedContainer.objects.filter(title=title).delete()
    info = {} #Set original title of setname

    injectedDataframe = injected_data_container.injected.to_json()
    injected_data_set = InjectedContainer(title=title, injectedContainer_json=injected_data_container.to_json(),
                                          description=description,original_data_set=setname)
    injected_data_set.save()
    return JsonResponse({"success": True})
