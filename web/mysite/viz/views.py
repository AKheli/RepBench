import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import pandas as pd
from pandas import DataFrame
from algorithms import algo_mapper
from web.mysite.viz.forms.injection_form import ParamForm, InjectionForm
from Injection.injection_methods.basic_injections import add_anomalies

data_set = "bafu5k"  # request.POST.get("dataset","bafu5k")
df: DataFrame = pd.read_csv(f"../../data/train/{data_set}.csv")


def get_data(request):
    data = {
        'series': [{"visible": i < 5, "id": col_name, "name": col_name, "data": list(df[col_name])} for (i, col_name) in
                   enumerate(df.columns)]}
    return JsonResponse(data)


def param_forms(df):
    param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        param_forms[alg] = ParamForm(**param_range)
    return param_forms


def index(request):
    if request.POST.get("type", None) == "injection":
        print("JSSSSOOOON RESPONSE")
        df: DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
        data = {'series': [{"name": col_name, "data": list(df[col_name])} for col_name in df.columns]}
        return JsonResponse(data)

    elif request.POST.get("type", None) == "load_data_set":
        df: DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
        data = {
            'series': [{"visible": i < 5, "id": str(i), "name": col_name, "data": list(df[col_name])} for (i, col_name)
                       in enumerate(df.columns)]}
        return JsonResponse(data)
    else:

        df: DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
        context = {"table_data": [],
                   'series': [{"name": col_name, "data": list(df[col_name])} for col_name in df.columns]}

        context["forms"] = param_forms(df)
        context["injection_form"] = InjectionForm(list(df.columns))
    return render(request, 'index.html', context=context)


def inject(request):
    df: DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
    post = request.POST
    col_name = post.get("data_columns")
    col = df[col_name]
    factor = float(post.get("factor"))
    ratio = float(post.get("ratio"))
    a_type = post.get("anomaly")
    n_anomalies = int(ratio * df.shape[0] / 30) + 1
    col_injected, _ = add_anomalies(col,
                                    a_type=a_type,
                                    a_factor=factor,
                                    a_len=30,
                                    n_anomalies=n_anomalies,
                                    fill_na=True)

    injected_series = {
        'series': {"linkedTo": col_name,
                   "id": f"{col_name}_injected",
                   "name": f"{col_name}_injected",
                    "data": col_injected.replace({np.nan: None}).values.tolist(),
                    "color": "red",
                   "rmse" :1
                   },
        'rmse' : 0.1
    }
    print(injected_series)

    return JsonResponse(injected_series)
