from django.urls import path
from . import views

app_name = "circles"

urlpatterns = [
    path("", views.home, name="index"),
    path("activities/", views.activities_list, name="activities_list"),
    path("events/", views.events_calendar, name="events_calendar"),
    path("board/", views.board, name="board"),
    path("contacts/", views.contacts, name="contacts"),
]