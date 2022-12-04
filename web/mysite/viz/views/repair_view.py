import random

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from pandas import DataFrame

from data_methods.data_class import DataContainer
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from web.mysite.viz.forms.alg_param_forms import  SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField
from web.mysite.viz.forms.injection_form import  InjectionForm
from Injection.injection_methods.basic_injections import add_anomalies
import json
from web.mysite.viz.BenchmarkMaps.create_repair_output import repair_from_None_series
from web.mysite.viz.ts_manager.HighchartsMapper import map_injected_series, map_repair_data
from web.mysite.viz.views.dataset_views import DatasetView


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p




class RepairView(DatasetView):
    template = "repair.html"
    error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_rmse": "RMSE on Anomaly",
                 "runtime": "runtime"}

    ParamForms = {"SCREEN": SCREENparamForm(), "RPCA": RPCAparamForm(), "CDrec": CDparamForm(), "IMR": IMRparamField()}

    def data_set_repair_and_injection_context(self, df):
        context = {}
        context["alg_forms"] = self.ParamForms
        context["injection_form"] = InjectionForm(list(df.columns))
        return context

    def get(self, request, setname="BAFU"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_repair_and_injection_context(df))
        return render(request, self.template , context=context)


    @staticmethod
    def inject_data(request, setname):
        post = request.POST
        col_name = post.get("data_columns")


        data_container = DatasetView.load_data_container(setname)
        df = data_container.norm_data
        col_norm = df[col_name]
        original_col = data_container.original_data[col_name]

        #anomaly injection values
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

        col_injected, _ = add_anomalies(col_norm,
                                        a_type=a_type,
                                        a_factor=factor,
                                        a_len=30,
                                        n_anomalies=n_anomalies,
                                        fill_na=True, seed=seed)


        injected_series = map_injected_series(col_injected, col_name, data_container)
        print(injected_series)
        return JsonResponse({"injected_series" : injected_series})


    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container = injected_container_None_Series(df_norm, injected_series)

        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]

        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}
        repaired_series = map_repair_data(repair, injected_data_container, alg_name, links, df_original)
        output = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}


        context = {"metrics": output["metrics"]}
        output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')
        return JsonResponse(output)



