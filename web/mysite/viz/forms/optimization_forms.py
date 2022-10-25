from django import forms

from algorithms import algo_mapper

error_choices = [("full_rmse", "RMSE"), ("mae", "MAE"), ("partial_rmse", "RMSE on anomaly")]


class BayesianOptForm(forms.Form):
    n_initial_points = forms.IntegerField(label="n start", initial=20)
    n_calls = forms.IntegerField(label="n", initial=20)
    error_loss = forms.CharField(label='Anomaly Type', widget=forms.Select(choices=error_choices,
                                                                           attrs={
                                                                               "class": 'form-control multi-anomaly'}))


def bayesian_opt_param_forms_inputs(df):
    b_param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        b_param_forms[alg] = [{"param_name": k, "min": min(v), "max": max(v)} for k, v in param_range.items()]
    return b_param_forms
