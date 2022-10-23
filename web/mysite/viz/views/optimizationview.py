import json

from django.shortcuts import render
from pandas import DataFrame

from django import forms
from web.mysite.viz.BenchmarkMaps.create_repair_output import repair_from_None_series
from web.mysite.viz.forms.injection_form import ParamForm, InjectionForm
import pandas as pd
from web.mysite.viz.forms.optimization_forms import BayesianOptForm, bayesian_opt_param_forms_inputs




def optimization_view(request, setname="bafu5k"):
    df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
    context = {"dataset": setname,
               "bayesian_opt_form" : BayesianOptForm(),
               "b_opt_param_forms": bayesian_opt_param_forms_inputs(df),
               "injection_form": InjectionForm(list(df.columns))}

    return render(request, 'optimization.html', context=context)


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


def optimize(request,dataset="bafu5k"):
    post = request.POST.dict()
    injected_series = json.loads(post.pop("injected_series"))
    params = {k: parse_param_input(v) for k, v in post.items()}

    param_ranges = {}
    for key,v in post.items():
        if "-min" in key:
            param_ranges[key.split("-")[0]] = parse_param_input(v)

    for key,v in post.items():
        if "-max" in key:
            param_ranges[key.split("-")[0]] = (param_ranges[key.split("-")[0]],parse_param_input(v))

    print(param_ranges)
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")
    output = repair_from_None_series(params, df, *injected_series.values())
    # context = {"metrics": output["metrics"]}
    # output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')
    # return JsonResponse(output)
