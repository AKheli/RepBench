## views for vizualization of subcomponents
import pandas as pd
from django.shortcuts import render
from pandas import DataFrame
from web.mysite.viz.forms.injection_form import InjectionForm


def injection_form_view(request, dataset = "bafu5k"):
    df: DataFrame = pd.read_csv(f"data/train/{dataset}.csv")
    context = { "dataset":dataset, "injection_form": InjectionForm(list(df.columns))}
    return render(request, 'sub/injectionForm.html', context=context)


