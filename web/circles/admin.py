from django.contrib import admin
from .models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_public", "owner", "created_at")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "description", "owner__username")
    prepopulated_fields = {"slug": ("name",)}