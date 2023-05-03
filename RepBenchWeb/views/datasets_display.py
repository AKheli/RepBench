from django.shortcuts import render

from RepBenchWeb.models import DataSet, InjectedContainer


# @staticmethod
# def optimization_datasets(request=None):
#     context = {}
#     context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
#                                     for dataSet in InjectedContainer.objects.all() if
#                                     dataSet.title is not None and dataSet.title != "" and dataSet.get_info()["length"] < 1000}
#     context["type"] = type
#     return render(request, 'data_set_options/optimizationDatasets.html', context=context)

def display_optimization_datasets(request=None, synthetic=False):
    context = {"syntheticDatasets": {dataSet.title: dataSet.get_info()
                                     for dataSet in InjectedContainer.objects.all() if
                                     dataSet.title is not None and dataSet.title != ""},

                "option" : "Optimize"}



    return render(request, 'data_set_options/displayDatasetsSynthetic.html', context=context)
