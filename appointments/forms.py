from django import forms
from django.utils import timezone

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    appointment_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Appointment
        fields = ['service', 'stylist_name', 'appointment_datetime', 'notes']

    def clean_appointment_datetime(self):
        appointment_datetime = self.cleaned_data['appointment_datetime']
        if appointment_datetime <= timezone.now():
            raise forms.ValidationError('Please choose a future date and time.')
        return appointment_datetime
