from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "circles"

urlpatterns = [
    # Home
    path("", views.home, name="index"),

    # Circles - NOTE THE ORDER!
    path("c/", views.CircleListView.as_view(), name="circle_list"),
    path("c/new/", views.CircleCreateView.as_view(), name="circle_create"),  # ADD THIS
    path("c/<slug:slug>/", views.CircleDetailView.as_view(), name="circle_detail"),

    # Posts (scoped to circle)
    path("c/<slug:slug>/posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("c/<slug:slug>/p/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),

    # Comments
    path("c/<slug:slug>/p/<int:pk>/comment/", views.CommentCreateView.as_view(), name="comment_create"),

    # Voting
    path("c/<slug:slug>/p/<int:pk>/upvote/", views.PostVoteView.as_view(), {"value": 1}, name="post_upvote"),
    path("c/<slug:slug>/p/<int:pk>/downvote/", views.PostVoteView.as_view(), {"value": -1}, name="post_downvote"),

    # Membership
    path("c/<slug:slug>/join/", views.JoinCircleView.as_view(), name="circle_join"),
    path("c/<slug:slug>/leave/", views.LeaveCircleView.as_view(), name="circle_leave"),

    # Activities CRUD
    path("activities/", views.ActivityListView.as_view(), name="activities_list"),
    path("activities/new/", views.ActivityCreateView.as_view(), name="activity_create"),
    path("activities/<int:pk>/edit/", views.ActivityUpdateView.as_view(), name="activity_update"),
    path("activities/<int:pk>/delete/", views.ActivityDeleteView.as_view(), name="activity_delete"),
    
    # Events CRUD
    path("events/", views.events_calendar, name="events_calendar"),
    path("events/list/", views.EventListView.as_view(), name="events_list"),
    path("events/new/", views.EventCreateView.as_view(), name="event_create"),  # This line must exist
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
    
    # Placeholder views for navbar
    path("board/", views.bulletin_board, name="board"),
    
    # Search
    path("search/", views.search, name="search"),
    
    # Emergency
    path("emergency/", views.emergency_contacts, name="emergency_contacts"),
    path("emergency/new/", views.emergency_contact_create, name="emergency_contact_create"),

    # Legacy aliases (so older templates that use 'contacts' still work)
    path("contacts/", views.emergency_contacts, name="contacts"),
    path("contacts/new/", views.emergency_contact_create, name="contacts_new"),
    
    # Authentication URLs
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]