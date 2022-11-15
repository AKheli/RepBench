from django import forms
from django.forms import NumberInput

DATA_SET_CHOISES = [
    ('bafu5k', 'bafu5k'),
    ('elec', 'elec'),
    ('humidity', 'humidity'),
    ('msd1_5', 'msd1_5'),
]


# class UserForm(forms.Form):
#     dataset = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=DATA_SET_CHOISES))




ANOMALY_CHOICES = [
    ("shift", "shift"),
    ("outlier", "outlier"),
    ("distortion", "distortion"),
]


class InjectionForm(forms.Form):
    ratio = forms.FloatField(label='ratio', min_value=0, max_value=1, initial=0.1, widget=NumberInput(
        attrs={'id': "ratio_id", 'min': 1, 'max': 0, 'step': '0.05'}))
    factor = forms.FloatField(min_value=0, initial=3)
    anomaly = forms.CharField(label='Anomaly Type', widget=forms.Select(choices=ANOMALY_CHOICES, attrs={
        "class": 'multi-anomaly'}))

    def __init__(self, data_columns, ts_name="bafu", *args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        self.fields["data_columns"] = forms.CharField(label="Column",
                                                      widget=forms.Select(choices=[(i, i) for i in data_columns]))
        self.fields["data_set"] = forms.CharField(widget=forms.HiddenInput(), required=False, initial=ts_name)
        self.fields["seed"] = forms.IntegerField(label='seed',required=False, widget=forms.NumberInput(
                attrs={'title': 'Enter numbers Only '}))
