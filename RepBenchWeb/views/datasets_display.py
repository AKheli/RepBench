from django.shortcuts import render
from RepBenchWeb.views.config import *
from RepBenchWeb.models import DataSet, InjectedContainer

def display_optimization_datasets(request=None, synthetic=False):
    context = {"syntheticDatasets": {dataSet.title: dataSet.get_info()
                                     for dataSet in InjectedContainer.objects.all() if
                                     dataSet.title is not None and dataSet.title != ""},

                "option" : "Optimize"}

    return render(request, DISPLAY_OPTIMIZATION_DATASETS_TEMPLATE, context=context)


