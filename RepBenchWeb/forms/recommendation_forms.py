# automl_settings = {
#     "time_budget": time_budget,  # in seconds
#     "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
#     "task": 'classification',
#     "log_file_name": "recommendation/logs/flaml.log",
#     "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
# }

from django import forms

ESTIMATOR_CHOICES = [
    ('lgbm', 'LGBM'),
    ('rf', 'Random Forest'),
    ('xgboost', 'XGBoost'),
    ('extra_tree', 'Extra Tree'),
    ('lrl1', 'Logisitc Regression')
]

RayTunes_ESTIMATOR_CHOICES = [
    ('LGBM', 'LGBM'),
    ('RandomForest', 'Random Forest'),
    ('ExtraTrees', 'Extra Tree'),
    ('LogisticRegression', 'Logistic Regression')
]

FEATURE_CHOICES = [ ("catch22","Catch22"), ("tsfresh_minimal","TSFreshMinimal"),("tsfresh_selected","TSFresh")]
METRIC_CHOICES = [('accuracy', 'Accuracy'), ('micro_f1', 'Micro F1'), ('macro_f1', 'Macro F1')]
TASK_CHOICES = [('classification', 'classification')]  # add more if needed


class AutomlSettingsForm(forms.Form):
    time_budget = forms.IntegerField(label='Time Budget (seconds)', initial=60, widget=forms.NumberInput(
        attrs={'id': "time_budget_id", 'min': 0, "class": 'form-control'}))
    metric = forms.CharField(label='Metric', initial='accuracy', widget=forms.Select(choices=METRIC_CHOICES, attrs={
        "class": 'form-control'}))
    # task = forms.CharField(initial='classification', widget=forms.HiddenInput(), required=False)
    estimator_list = forms.MultipleChoiceField(label='Estimators',
                                               initial=[choice[1] for choice in ESTIMATOR_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'multi-checkbox', "name": 'estimator_list[]'}),
                                               choices=ESTIMATOR_CHOICES
                                               )

    features = forms.MultipleChoiceField(label='Features',
                                               initial=[choice[0] for choice in FEATURE_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'kt-checkbox', "name": 'estimator_list[]'}),
                                               choices=FEATURE_CHOICES
                                               )
    def __init__(self, *args, **kwargs):
        super(AutomlSettingsForm, self).__init__(*args, **kwargs)
        self.fields['estimator_list'].initial = [choice[0] for choice in ESTIMATOR_CHOICES]


class RayTuneSettingsForm(forms.Form):
    ray_tunes_time_budget = forms.IntegerField(label='Time Budget (secondss)', initial=60, widget=forms.NumberInput(
        attrs={'id': "time_budget_id", 'min': 0, "class": 'form-control'}))
    ray_tunes_metric = forms.CharField(label='Metric', initial='accuracy', widget=forms.Select(choices=METRIC_CHOICES, attrs={
        "class": 'form-control'}))
    # task = forms.CharField(initial='classification', widget=forms.HiddenInput(), required=False)
    ray_tunes_estimator_list = forms.MultipleChoiceField(label='Estimator',
                                               initial=[choice[1] for choice in RayTunes_ESTIMATOR_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'form-control', "name": 'estimator'}),
                                               choices=RayTunes_ESTIMATOR_CHOICES
                                               )

    ray_tunes_features = forms.ChoiceField(label='Features',
                                               initial=[choice[0] for choice in FEATURE_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'kt-checkbox', "name": 'estimator_list[]'}),
                                               choices=FEATURE_CHOICES
                                               )
    def __init__(self, *args, **kwargs):
        super(RayTuneSettingsForm, self).__init__(*args, **kwargs)
        self.fields['ray_tunes_estimator_list'].initial = [choice[0] for choice in RayTunes_ESTIMATOR_CHOICES]
