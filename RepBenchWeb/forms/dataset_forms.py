from django import forms
from RepBenchWeb.models import DataSet , InjectedContainer




DATASET_CHOICES =  [ (dataset.title,dataset.title)   for dataset in DataSet.objects.all() ]
INJECTED_DATASET_CHOICES = [ (dataset.title,dataset.title)   for dataset in InjectedContainer.objects.all() ]


class DataSetsForm(forms.Form):
    dataset = forms.CharField(label='Dataset', widget=forms.Select(choices=DATASET_CHOICES, attrs={
        "class": 'form-control', "id": "anomaly_id",
        "myInfo": "Select the dataset to be used."}))

class InjectedDataSetForm(forms.Form):
    dataset = forms.CharField(label='Dataset', widget=forms.Select(choices=INJECTED_DATASET_CHOICES, attrs={
        "class": 'form-control', "id": "selected_dataset_title",
        "myInfo": "Select the dataset to be used."}))
