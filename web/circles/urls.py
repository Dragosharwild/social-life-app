from django.urls import path
from . import views

app_name = "circles"

urlpatterns = [
    path("", views.home, name="index"),
    
    # Circles
    path("c/", views.CircleListView.as_view(), name="circle_list"),
    path("c/<slug:slug>/", views.CircleDetailView.as_view(), name="circle_detail"),
    
    # Posts
    path("c/<slug:slug>/posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("c/<slug:slug>/p/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    
    # Activities CRUD
    path("activities/", views.ActivityListView.as_view(), name="activities_list"),
    path("activities/new/", views.ActivityCreateView.as_view(), name="activity_create"),
    path("activities/<int:pk>/edit/", views.ActivityUpdateView.as_view(), name="activity_update"),
    path("activities/<int:pk>/delete/", views.ActivityDeleteView.as_view(), name="activity_delete"),

    # Existing pages
    path("activities/", views.activities_list, name="activities_list"),
    path("events/", views.events_calendar, name="events_calendar"),
    path("board/", views.board, name="board"),
    path("contacts/", views.contacts, name="contacts"),
]