from django import forms

from algorithms import algo_mapper

error_choices = [("rmse", "RMSE"), ("mae", "MAE"), ("partial_rmse", "RMSE on anomaly")]


class BayesianOptForm(forms.Form):
    n_initial_points = forms.IntegerField(label="n start", initial=20)
    n_initial_points.widget.attrs.update({ "class": 'multi-anomaly', "style": "width: 90px"})

    n_calls = forms.IntegerField(label="n", initial=20)
    n_calls.widget.attrs.update({ "class": 'multi-anomaly', "style": "width: 90px"})
    error_loss = forms.CharField(label='Loss', widget=forms.Select(choices=error_choices))


def bayesian_opt_param_forms_inputs(df):
    b_param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        b_param_forms[alg] = [{"param_name": k, "min": min(v), "max": max(v)} for k, v in param_range.items()]
    return b_param_forms
