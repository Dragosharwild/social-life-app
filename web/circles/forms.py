from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "day_of_week", "start_time", "end_time", "location"]