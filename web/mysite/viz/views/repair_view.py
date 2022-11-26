import random
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from pandas import DataFrame

from web.mysite.viz.forms.alg_param_forms import ParamForms
from web.mysite.viz.forms.injection_form import  InjectionForm
from Injection.injection_methods.basic_injections import add_anomalies
import json
from web.mysite.viz.BenchmarkMaps.create_repair_output import repair_from_None_series
from web.mysite.viz.views.dataset_views import DatasetView
from web.mysite.viz.views.optimizationview import opt_JSONRespnse


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p





class RepairView(DatasetView):

    def data_set_repair_and_injection_context(self, df):
        context = {}
        context["alg_forms"] = ParamForms
        context["injection_form"] = InjectionForm(list(df.columns))
        return context

    def get(self, request, setname="bafu5k"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_repair_and_injection_context(df))
        print(context)
        return render(request, 'repair.html', context=context)

    @staticmethod
    def inject_data(request, setname):
        token = request.POST.get("csrfmiddlewaretoken")
        import web.mysite.viz.BenchmarkMaps.Optjob as OptJob
        try:
            status, data = OptJob.retrieve_results(token)
            #log to javascript console
            print("EEEEEEEEEEEEEEEEEYYYY")
            print(data)
        except Exception as e:
            o = OptJob
            print("exception")
            print(e)
            pass
        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
        post = request.POST
        col_name = post.get("data_columns") #.strip() #todo check why input is not stripped
        print(df.columns)
        col = df[col_name]
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

        col_injected, _ = add_anomalies(col,
                                        a_type=a_type,
                                        a_factor=factor,
                                        a_len=30,
                                        n_anomalies=n_anomalies,
                                        fill_na=True, seed=seed)

        injected_series = {
            'series': {"linkedTo": col_name,
                       "id": f"{col_name}_injected",
                       "name": f"{col_name}_injected",
                       "data": col_injected.replace({np.nan: None}).values.tolist(),
                       "color": "red",
                       },
            'rmse': 0.1
        }
        return JsonResponse(injected_series)


    @staticmethod
    def repair_data(request, setname):

        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}
        output = repair_from_None_series(alg_type , params, df, *injected_series.values())
        context = {"metrics": output["metrics"]}
        output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')
        return JsonResponse(output)



