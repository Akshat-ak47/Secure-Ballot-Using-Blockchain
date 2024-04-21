# app1/forms.py

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'num_teams', 'event_purpose']  # Include 'num_teams' field

    def clean_num_teams(self):
        num_teams = self.cleaned_data.get('num_teams')
        if num_teams <= 0:
            raise forms.ValidationError("Number of teams must be greater than zero.")
        return num_teams
