from django.http import JsonResponse
from django.shortcuts import render
import json

from algorithms.Dimensionality_Reduction.dimensionality_Reduction_estimator import DimensionalityReductionEstimator
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from web.mysite.viz.forms.alg_param_forms import RPCAparamForm, CDparamForm
from web.mysite.viz.ts_manager.HighchartsMapper import map_repair_data, reverse_norm
from web.mysite.viz.views.dataset_views import DatasetView
from web.mysite.viz.views.repair_view import RepairView, parse_param_input


class DimensionalityReductionView(RepairView):
    template = "dimensionalityReductionVisualization.html"
    ParamForms = {"RPCA": RPCAparamForm(), "CDrec": CDparamForm()}

    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container = injected_container_None_Series(df_norm, injected_series)

        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]
        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if
                         k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}
        repaired_series = map_repair_data(repair, injected_data_container, alg_name, links, df_original)
        context = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        context["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')

        estimator: DimensionalityReductionEstimator = repair_retval["estimator"]
        reductions = estimator.reduction_per_classification_iter
        context["reductions"] = [
            [{"linkedTo": col, "data": list(reverse_norm(df_reduced[col], df_original[col])), "norm_data": list(df_reduced[col])} for col
             in df_reduced.columns]
            for df_reduced in reductions]


        return JsonResponse(context, encoder=DimensionalityReductionView.encoder)
