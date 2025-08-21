from django import forms
from .models import Activity, Post

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "day_of_week", "start_time", "end_time", "location"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "link_url"]