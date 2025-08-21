from django.contrib import admin
from .models import Circle, Post, Activity

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_public", "owner", "created_at")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "description", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "circle", "author", "score", "created_at")
    list_filter = ("circle",)
    search_fields = ("title", "body", "author__username", "circle__name")
    
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "day_of_week", "start_time", "end_time", "location", "updated_at")
    list_filter = ("day_of_week",)
    search_fields = ("title", "location")