from django import forms

class UploadFilesForm(forms.Form):
    file1 = forms.FileField(label="File 1 (Required)")
    file2 = forms.FileField(label="File 2 (Optional)", required=False)
    file3 = forms.FileField(label="File 3 (Optional)", required=False)
