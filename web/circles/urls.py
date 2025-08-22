from django.urls import path
from . import views

app_name = "circles"

urlpatterns = [
    # Home
    path("", views.home, name="index"),

    # Circles
    path("c/", views.CircleListView.as_view(), name="circle_list"),
    path("c/<slug:slug>/", views.CircleDetailView.as_view(), name="circle_detail"),

    # Posts (scoped to circle)
    path("c/<slug:slug>/posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("c/<slug:slug>/p/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),

    # Comments
    path("c/<slug:slug>/p/<int:pk>/comment/", views.CommentCreateView.as_view(), name="comment_create"),

    # Voting
    path("c/<slug:slug>/p/<int:pk>/upvote/", views.PostVoteView.as_view(), {"value": 1}, name="post_upvote"),
    path("c/<slug:slug>/p/<int:pk>/downvote/", views.PostVoteView.as_view(), {"value": -1}, name="post_downvote"),

    # Activities CRUD
    path("activities/", views.ActivityListView.as_view(), name="activities_list"),
    path("activities/new/", views.ActivityCreateView.as_view(), name="activity_create"),
    path("activities/<int:pk>/edit/", views.ActivityUpdateView.as_view(), name="activity_update"),
    path("activities/<int:pk>/delete/", views.ActivityDeleteView.as_view(), name="activity_delete"),
]