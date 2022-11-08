import os

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from pandas import DataFrame

from web.mysite.viz.forms.injection_form import InjectionForm
from web.mysite.viz.views.indexview import param_forms


def test_view(request):
    # transform request.body to dictionary
    a = int(request.GET.get("a", 0)) + 1
    if request.method == "POST":
        a = request.POST.dict()
        print(a)

    return render(request, 'test.html', context={"a": a})


def test_inner_view(request, dataset="bafu5k"):
    """
    return html from the test2.html with context
    """
    index = int(request.GET.get("index", 0))
    a = 20
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")
    context = {"dataset": dataset, "correlation": df.corr().round(3).to_html(classes=["table table-sm table-dark"]),
               "index": index}
    return render(request, 'sub/test2.html', context=context)


# to fetch whitout page reload
def get_data(request, dataset="bafu5k"):
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")
    viz = int(request.GET.get("viz", 5))

    data = {
        'series': [{"visible": i < viz, "id": col_name, "name": col_name, "data": list(df[col_name])} for (i, col_name)
                   in
                   enumerate(df.columns)],
       }
    return JsonResponse(data)



def display_datasets(request=None):
    data_files = os.listdir("data/train")

    context = {"datasets": {f.split(".")[0]: {"full_file_name": f} for f in data_files}}

    return render(request, 'displayDatasets.html', context=context)



def viz_dataset(request, setname):
    df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
    viz = int(request.GET.get("viz", 5))
    correlation_html  =  df.corr().round(3).to_html(classes=["table table-sm table-dark"])
    context = {
        "dataset": setname,
        "viz": viz,
        "data_title": setname,
        "correlation": correlation_html,}
    print("original context",context)
    return render(request, 'displayDataset.html', context=context)
