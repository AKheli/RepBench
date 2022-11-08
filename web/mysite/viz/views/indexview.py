import random
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from pandas import DataFrame
from algorithms import algo_mapper
from web.mysite.viz.forms.injection_form import ParamForm, InjectionForm
from Injection.injection_methods.basic_injections import add_anomalies
import json
from web.mysite.viz.BenchmarkMaps.create_repair_output import repair_from_None_series





def param_forms(df):
    param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        form = ParamForm(alg, **param_range)
        param_forms[alg] = form
    return param_forms


def index(request, setname="bafu5k"):
    df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
    context = {"dataset": setname,
               "forms": param_forms(df), "injection_form": InjectionForm(list(df.columns))}
    return render(request, 'index.html', context=context)


def inject(request, dataset):
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")
    post = request.POST
    col_name = post.get("data_columns")
    col_index = list(df.columns).index(col_name)
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
                   "rmse": 1
                   },
        'rmse': 0.1
    }
    print(injected_series)

    return JsonResponse(injected_series)


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


def repair(request, dataset):
    post = request.POST.dict()
    injected_series = json.loads(post.pop("injected_series"))
    params = {k: parse_param_input(v) for k, v in post.items()}
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")

    output = repair_from_None_series(params, df, *injected_series.values())
    context = {"metrics": output["metrics"]}
    output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')
    return JsonResponse(output)
