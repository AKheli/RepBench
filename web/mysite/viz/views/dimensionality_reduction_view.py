import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import json

from Injection.injected_data_part import InjectedDataContainer
from algorithms.Dimensionality_Reduction.dimensionality_Reduction_estimator import DimensionalityReductionEstimator
from testing_frame_work.repair import AnomalyRepairer
from web.mysite.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from web.mysite.viz.forms.alg_param_forms import RPCAparamForm, CDparamForm
from web.mysite.viz.ts_manager.HighchartsMapper import map_repair_data, reverse_norm
from web.mysite.viz.views.dataset_views import DatasetView
from web.mysite.viz.views.repair_view import RepairView, parse_param_input
from data_methods.data_class import normalize_f


class DimensionalityReductionView(RepairView):
    template = "dimensionalityReductionVisualization.html"
    ParamForms = {"RPCA": RPCAparamForm(), "CDrec": CDparamForm()}

    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")
        threshold = post["threshold"]

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container: InjectedDataContainer = injected_container_None_Series(df_norm, injected_series)

        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]
        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if
                         k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        original_to_injected_links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}

        repaired_series = map_repair_data(repair, injected_data_container, alg_name, original_to_injected_links,
                                          df_original)
        context = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        context["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')

        ### Extract Reduced Series
        estimator: DimensionalityReductionEstimator = repair_retval["estimator"]

        ## same way as done by the estimator
        # def z_score(x, threshold):
        #     x_abs = np.abs(x)
        #     x_normalized = (x_abs - np.mean(x_abs)) / np.std(x_abs)
        #     return x_normalized > threshold

        def z_score(x):
            x_abs = np.abs(x)
            x_normalized_diff = (x_abs - np.mean(x_abs)) / np.std(x_abs)
            print(x_normalized_diff.std())
            print(sum(x_normalized_diff > float(threshold)))

            return x_normalized_diff
        normalized_injected, _ = normalize_f(injected_data_container.injected)

        reductions = estimator.reduction_per_classification_iter
        context["reductions"] = [
            [{"name": f"{col}_red_{r_iter + 1}",
              "linkedTo": col+"repair"+alg_name,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col]),

              }
             for i, col in enumerate(df_reduced.columns)]
            for r_iter, df_reduced in enumerate(reductions) if r_iter in [0,4,9]]

        df_reduced = reductions[-1]
        context["final_reductions"] = \
            [{"name": f"{col}reduced",
              "linkedTo": col+"repair"+alg_name,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col]),
              "diff_norm": list(z_score(df_reduced[col] - normalized_injected[col]))
              if i in injected_data_container.injected_columns else None,
              "threshold": threshold,
              "classified" : list(estimator.anomaly_matrix[:,i]*1)
              }
             for i, col in enumerate(df_reduced.columns) if
             i in injected_data_container.injected_columns]

        Anomalies = injected_data_container.class_df.values
        classified = estimator.anomaly_matrix
        TP = np.sum(np.logical_and(classified,Anomalies))
        TN = np.sum( np.logical_and(~classified,~Anomalies))

        FP = np.sum(classified == 1) - TP
        FN = np.sum( np.logical_and(~classified,Anomalies))
        context["TP"] = TP
        context["FP"] = FP
        context["FN"] = FN
        context["TN"] = TN

        return JsonResponse(context, encoder=DimensionalityReductionView.encoder)
