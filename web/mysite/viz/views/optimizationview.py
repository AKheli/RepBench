import json

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from pandas import DataFrame
from web.mysite.viz.BenchmarkMaps.optimization import optimize_from_None_series
from web.mysite.viz.forms.injection_form import  InjectionForm
import pandas as pd
from web.mysite.viz.forms.optimization_forms import BayesianOptForm, bayesian_opt_param_forms_inputs
from web.mysite.viz.views.dataset_views import DatasetView




def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


class OptimizationView(DatasetView):

    def load_data_set(self, setname):
        df: DataFrame = pd.read_csv(f"data/opt/{setname}.csv")
        return df

    def create_opt_context(self, df):
        opt_context = {"bayesian_opt_form": BayesianOptForm(),
                   "b_opt_param_forms": bayesian_opt_param_forms_inputs(df),
                   "injection_form": InjectionForm(list(df.columns))}
        return opt_context

    def get(self, request, setname="bafu5k"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.create_opt_context(df))
        print(context)
        return render(request, 'optimization.html', context=context)


    def optimize(request, setname="bafu5k"):
        post = request.POST.dict()
        print(post)
        injected_series = json.loads(post.pop("injected_series"))
        param_ranges = {}
        for key, v in post.items():
            if  key.endswith("-min"):
                param_ranges[key.split("-")[0]] = parse_param_input(v)
        for key, v in post.items():
            if key.endswith("-max"):
                param_ranges[key.split("-")[0]] = (param_ranges[key.split("-")[0]], parse_param_input(v))

        error_loss = post.pop("error_loss")
        alg_type = post.pop("alg_type")
        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")

        bayesian_opt_inputs = {"n_calls": int(post.pop("n_calls")), "n_initial_points": int(post.pop("n_initial_points")),
                               "error_score": error_loss}
        output = optimize_from_None_series(param_ranges, alg_type, bayesian_opt_inputs, df, *injected_series.values())

        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return json.JSONEncoder.default(self, obj)

        output = json.loads(json.dumps(output, cls=NpEncoder))
        return JsonResponse(output)


