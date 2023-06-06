from django.http import JsonResponse
from django.shortcuts import render

from RepBenchWeb.forms.dataset_forms import InjectedDataSetForm
from RepBenchWeb.views.config import *
from RepBenchWeb.forms.recommendation_forms import FLAMLSettingsForm, RayTuneSettingsForm
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.synthetic_dataset_view import SyntheticDatasetView
from injection.injected_data_container import InjectedDataContainer
from testing_frame_work.data_methods.data_class import DataContainer


class RecommendationView(SyntheticDatasetView):
    templates = [FLAML_RECOMMENDATION_TEMPLATE, RAY_TUNE_RECOMMENDATION_TEMPLATE]
    recommender_file_name = ""

    def get(self, request, type="FLAML"):
        # data_object = InjectedContainer.objects.get(title=setname)
        # injected_data_container: InjectedDataContainer = data_object.injected_container
        # data_container = DataContainer(injected_data_container.truth)
        # df = data_container.original_data
        context = {}
        # context["data_info"] =  InjectedContainer.objects.get(title=setname).get_info()
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        # context["data_fetch_url_name"] = self.data_fetch_url_name
        # context["injected_data_set_info"] = self.data_set_info_context(setname)

        context["flaml_settings_form"] = FLAMLSettingsForm()
        context["ray_tune_settings_form"] = RayTuneSettingsForm()
        context["injected_datasets_form"] = InjectedDataSetForm()

        if type == "FLAML":
            template = self.templates[0]
        else:
            template = self.templates[1]

        return render(request, template, context=context)

    @staticmethod
    def recommendation_datasets(request=None):
        context = {}
        context["datasets"] = {dataSet.title: dataSet.get_info()
                                        for dataSet in InjectedContainer.objects.all() if
                                        dataSet.title is not None and dataSet.title != "" }
        context["type"] = type
        return render(request, 'dataSetOptions/displayRecommendationDatasets.html', context=context)
