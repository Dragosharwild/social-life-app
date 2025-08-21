from django.shortcuts import render

def home(request):
    return render(request, "circles/index.html")

def activities_list(request):
    return render(request, "circles/activities_list.html", {"activities": []})

def events_calendar(request):
    return render(request, "circles/events_calendar.html")

def board(request):
    return render(request, "circles/board.html", {"posts": []})

def contacts(request):
    return render(request, "circles/contacts.html", {"contacts": []})