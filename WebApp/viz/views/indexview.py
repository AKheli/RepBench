import random
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from pandas import DataFrame
import pathlib
import sys

from algorithms import algo_mapper
from Injection.injection_methods.basic_injections import add_anomalies
import json
from WebApp.viz.BenchmarkMaps.create_repair_output import repair_from_None_series






def index(request, setname="bafu5k"):
    df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
    context = {}
    return render(request, 'index.html', context=context)

