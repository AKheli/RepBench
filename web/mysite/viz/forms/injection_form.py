from django import forms

from django import forms

DATA_SET_CHOISES= [
    ('bafu5k', 'bafu5k'),
    ('elec', 'elec'),
    ('humidity', 'humidity'),
    ('msd1_5', 'msd1_5'),
    ]

class UserForm(forms.Form):
    #first_name= forms.CharField(max_length=100)
    #last_name= forms.CharField(max_length=100)
    #email= forms.EmailField()
    dataset = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=DATA_SET_CHOISES))

