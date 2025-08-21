from django.contrib import admin
from .models import Activity, Event, Post, EmergencyContact

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "day_of_week", "start_time", "end_time", "location", "updated_at")
    list_filter = ("day_of_week",)

admin.site.register(Event)
admin.site.register(Post)
admin.site.register(EmergencyContact)