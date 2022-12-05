import json
import threading

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from pandas import DataFrame
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from web.mysite.viz.forms.injection_form import InjectionForm
import pandas as pd
from web.mysite.viz.forms.optimization_forms import BayesianOptForm, bayesian_opt_param_forms_inputs
from web.mysite.viz.views.dataset_views import DatasetView

import web.mysite.viz.BenchmarkMaps.Optjob as OptJob





def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p

class opt_JSONRespnse(JsonResponse):
    def __init__(self, data, callback=None, **kwargs):
        self.callback = callback
        super().__init__(data, encoder=self.NpEncoder, **kwargs)



class OptimizationView(DatasetView):
    template = "optimization.html"

    def create_opt_context(self, df):
        opt_context = {"bayesian_opt_form": BayesianOptForm(),
                       "b_opt_param_forms": bayesian_opt_param_forms_inputs(df),
                       "injection_form": InjectionForm(list(df.columns))}
        return opt_context

    def get(self, request, setname="BAFU"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.create_opt_context(df))
        return render(request, self.template, context=context)

    @staticmethod
    def optimize(request, setname="BAFU"):
        token = request.POST.get("csrfmiddlewaretoken")
        job_id = OptJob.add_job(token)
        post = request.POST.dict()

        # Bayesopt inputs
        n_initial_points = int(post["n_initial_points"])
        n_calls = int(post["n_calls"])
        error_loss = post["error_loss"]
        alg_type = post.pop("alg_type")

        injected_series = json.loads(post.pop("injected_series"))
        param_ranges = {}
        for key, v in post.items():
            if key.endswith("-min"):
                param_ranges[key.split("-")[0]] = parse_param_input(v)
        for key, v in post.items():
            if key.endswith("-max"):
                param_ranges[key.split("-")[0]] = (param_ranges[key.split("-")[0]], parse_param_input(v))

        df_norm = DatasetView.load_data_container(setname).norm_data
        injected_data_container = injected_container_None_Series(df_norm, injected_series)

        opt_callback = OptJob.start(job_id, param_ranges, alg_type, injected_data_container,
                                   n_calls=n_calls, n_initial_points=n_initial_points, error_loss=error_loss)
        t = threading.Thread(target=opt_callback)
        t.start()

        context = {
            "error_loss": error_loss,
            "alg_type": alg_type,
            "n_calls": n_calls,
            "n_initial_points": n_initial_points,
            "injected_series": injected_series,
            "param_ranges": param_ranges,
            "setname": setname,
        }
        return JsonResponse(context, encoder=OptimizationView.encoder)


def fetch_opt_results(request):
    token = request.POST.get("csrfmiddlewaretoken")
    status, data = OptJob.retrieve_results(token)
    if len(data) > 0:
        res = data.pop(0)
        res.update({"status": "running"})
        print("fetch_opt_results", res)
        print(res)
        print()
        return JsonResponse(res, encoder=OptimizationView.encoder)

    if status == "finished":
        return JsonResponse({"status": "DONE"}, encoder=OptimizationView.encoder)
    else:
        return JsonResponse({"status": "pending"}, encoder=OptimizationView.encoder)

