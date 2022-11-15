import numpy as np

from django import forms
from django.forms import NumberInput

from algorithms import algo_mapper
from algorithms.estimator import Estimator


type_form_mapper = {
    float: forms.FloatField,
    int: forms.IntegerField,
    str: forms.CharField,
    np.int : forms.IntegerField,
    np.float : forms.FloatField,
    np.float64 : forms.IntegerField,
}

class ParamForm(forms.Form):
    pass

def create_param_forms(df):
    estim : Estimator
    param_forms = {}
    for alg , estim in algo_mapper.items():
        param_form = ParamForm()
        param_form.fields["alg_type"] = forms.CharField(widget=forms.HiddenInput(), initial=alg)
        for param, v in estim().get_param_info(df).items():
            type_,min_,max_,default_,range_ = v
            param_form.fields[param] = type_form_mapper[type_](label=param, min_value=min_, max_value=max_, initial=default_,
                                                               widget=NumberInput( attrs={ 'title': 'Enter numbers Only '}))
        param_forms[alg] = param_form
    return param_forms
