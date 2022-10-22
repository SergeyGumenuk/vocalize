import datetime
from datetime import datetime as dt

from django import forms

from .models import Customer


TIME_SLOTS = ((dt.strptime('09:00:00', '%H:%M:%S').time(), '09:00'), (dt.strptime('09:30:00', '%H:%M:%S').time(), '09:30'),
              (dt.strptime('10:00:00', '%H:%M:%S').time(), '10:00'), (dt.strptime('10:30:00', '%H:%M:%S').time(), '10:30'),
              (dt.strptime('11:00:00', '%H:%M:%S').time(), '11:00'), (dt.strptime('11:30:00', '%H:%M:%S').time(), '11:30'),
              (dt.strptime('12:00:00', '%H:%M:%S').time(), '12:00'), (dt.strptime('12:30:00', '%H:%M:%S').time(), '12:30'),
              (dt.strptime('13:00:00', '%H:%M:%S').time(), '13:00'), (dt.strptime('13:30:00', '%H:%M:%S').time(), '13:30'),
              (dt.strptime('14:00:00', '%H:%M:%S').time(), '14:00'), (dt.strptime('14:30:00', '%H:%M:%S').time(), '14:30'),
              (dt.strptime('15:00:00', '%H:%M:%S').time(), '15:00'), (dt.strptime('15:30:00', '%H:%M:%S').time(), '15:30'),
              (dt.strptime('16:00:00', '%H:%M:%S').time(), '16:00'), (dt.strptime('16:30:00', '%H:%M:%S').time(), '16:30'),
              (dt.strptime('17:00:00', '%H:%M:%S').time(), '17:00'), (dt.strptime('17:30:00', '%H:%M:%S').time(), '17:30'),
              (dt.strptime('18:00:00', '%H:%M:%S').time(), '18:00'), (dt.strptime('18:30:00', '%H:%M:%S').time(), '18:30'),
              (dt.strptime('19:00:00', '%H:%M:%S').time(), '19:00'), (dt.strptime('19:30:00', '%H:%M:%S').time(), '19:30'),
              (dt.strptime('20:00:00', '%H:%M:%S').time(), '20:00'), (dt.strptime('20:30:00', '%H:%M:%S').time(), '20:30'),
              (dt.strptime('21:00:00', '%H:%M:%S').time(), '21:00'), (dt.strptime('21:30:00', '%H:%M:%S').time(), '21:30'),
              )


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'surname', 'photo']


class CalendarForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today(),
                           widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}))


class AddLessonForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today(),
                           widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}))
    time = forms.ChoiceField(choices=TIME_SLOTS)
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all())


class AddLessonQuickForm(forms.Form):
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all())
