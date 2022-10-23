import json

from django import forms
from algorithms import algo_mapper



class BayesianOptForm(forms.Form):
    n_initial_points = forms.IntegerField(label="n start")
    n_calls = forms.IntegerField(label="n")



class BayesianParamForm(forms.Form):
    def __init__(self, alg_type, **kwargs):
        super(BayesianParamForm, self).__init__()
        for k, v in kwargs.items():
            self.fields[f"{k}_lower"] = forms.IntegerField(label=f"{k} min")
            self.fields[f"{k}_upper"] = forms.IntegerField(label=f"max")
        self.fields["alg_type"] = forms.CharField(widget=forms.HiddenInput(), initial=alg_type)



def bayesian_opt_param_forms_inputs(df):
    b_param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        b_param_forms[alg] =  [{ "param_name" : k , "min" : min(v) , "max" : max(v)} for k, v in param_range.items() ]
    return b_param_forms



