from django import forms
from .models import Activity, Post, Comment, Event, EmergencyContact, BulletinBoard
from django.utils import timezone

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

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "starts_at", "ends_at", "location", "circle"]
        widgets = {
            "starts_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ends_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ["name", "type", "phone", "alt_phone", "is_24_7", "priority", "notes"]
        

class BulletinBoardForm(forms.ModelForm):
    class Meta:
        model = BulletinBoard
        fields = ['title', 'content', 'is_pinned', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expires_at'].required = False