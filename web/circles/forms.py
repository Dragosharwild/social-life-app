from django import forms
from .models import Activity, Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment…", "class": "form-control"}),
        }
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "day_of_week", "start_time", "end_time", "location"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "link_url"]