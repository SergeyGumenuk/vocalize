import datetime

from django import forms


class Calendar(forms.Form):
    #date = forms.DateField(initial=datetime.date.today(), input_formats=['YYYY-MM-DD'])
    date = forms.DateField(initial=datetime.date.today(),
                           widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}))


