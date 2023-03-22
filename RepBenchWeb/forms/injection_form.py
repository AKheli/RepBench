from django import forms
from django.forms import NumberInput
from django.utils.safestring import mark_safe

ANOMALY_CHOICES = [
    ("shift", "Shift"),
    ("outlier", "Outlier"),
    ("distortion", "Distortion"),
]


class RangeSliderInput(forms.TextInput):
    input_type = 'range'
    min_value = 5
    max_value = 100
    step = 1

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.pop('min_value', self.min_value)
        self.max_value = kwargs.pop('max_value', self.max_value)
        self.step = kwargs.pop('step', self.step)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['min'] = self.min_value
        context['widget']['attrs']['max'] = self.max_value
        context['widget']['attrs']['step'] = self.step
        return context

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        html = f'<div class="slider-container">{html}' \
               f'<span id="slider-value">{50}</span>' \
               f'</div>' + """
               '<script> $('#length-slider').on('input', function() {
                var value = $(this).val();
                $('#slider-value').text(' ' + value +' ');
                }); 
            </script>
            """
        return html


class InjectionForm(forms.Form):
    anomaly = forms.CharField(label='Anomaly Type', widget=forms.Select(choices=ANOMALY_CHOICES, attrs={
        "class": ''}))
    ratio = forms.FloatField(label='Ratio', min_value=0, max_value=1, initial=0.1, widget=NumberInput(
        attrs={'id': "ratio_id", 'min': 1, 'max': 0, 'step': '0.05'}))
    factor = forms.FloatField(min_value=0, initial=3)

    length = forms.IntegerField(widget=RangeSliderInput(attrs={'id': 'length-slider'}))


    def __init__(self, data_columns, ts_name="bafu", *args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        self.fields["data_columns"] = forms.MultipleChoiceField(
            label= mark_safe("Inject Anomalies For: &nbsp;"), # to add white space
            widget=forms.CheckboxSelectMultiple(),
            choices=[(i, i) for i in data_columns])

        self.fields["data_set"] = forms.CharField(widget=forms.HiddenInput(), required=False, initial=ts_name)
        self.fields["seed"] = forms.IntegerField(label='Seed', required=False, widget=forms.NumberInput(
            attrs={'title': 'Enter numbers Only '}))






class store_injection_form(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=1000, required=False
                                  , widget=forms.Textarea())

    class Meta:
        fields = ['title', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 4, 'rows': 2})
        }
