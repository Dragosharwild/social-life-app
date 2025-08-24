from django.contrib import admin
from .models import Circle, Post, Activity, Vote, Membership, Event, EmergencyContact

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
    
from .models import Circle, Post, Activity, Comment  # add Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("body", "author__username", "post__title")
    list_filter = ("created_at",)
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "value", "created_at")
    list_filter = ("value",)
    search_fields = ("post__title", "user__username")

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("circle", "user", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("circle__name", "user__username")
    
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "phone", "is_24_7", "priority", "updated_at")
    list_filter = ("type", "is_24_7")
    search_fields = ("name", "phone", "notes")
    ordering = ("priority", "name")