from django import forms

class UploadFilesForm(forms.Form):
    file1 = forms.FileField(label="File 1 (Required)", widget=forms.ClearableFileInput(attrs={'placeholder': 'No file selected'}))
    data_name = forms.CharField(label="Data Name (Required)", max_length=100)
    granularity = forms.CharField(label="Granularity (Required)", max_length=100, initial="1s")
    description = forms.CharField(label="Description (Required)", max_length=100, initial="No Description")
    ref_url = forms.CharField(label="Reference URL (Required)", max_length=100, initial="No Reference URL")
    url_text = forms.CharField(label="URL Text (Required)", max_length=100, initial="-")


    # file2 = forms.FileField(label="File 2 (Optional)", required=False)
    # file3 = forms.FileField(label="File 3 (Optional)", required=False)
