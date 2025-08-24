from datetime import datetime, timedelta
from calendar import HTMLCalendar

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import PostForm, ActivityForm, CommentForm, EventForm
from .models import (
    Circle, Post, Activity,
    Comment, Vote, Membership, Event
)

# Home
def home(request):
    return render(request, "circles/index.html")


# Events Calendar
def events_calendar(request):
    try:
        now = timezone.now()
        year = request.GET.get("year", now.year)
        month = request.GET.get("month", now.month)

        try:
            year = int(year)
            month = int(month)
        except (ValueError, TypeError):
            year = now.year
            month = now.month

        # prev/next month navigation
        prev_month = month - 1
        prev_year = year
        if prev_month == 0:
            prev_month = 12
            prev_year = year - 1

        next_month = month + 1
        next_year = year
        if next_month == 13:
            next_month = 1
            next_year = year + 1

        # Base calendar HTML
        cal = HTMLCalendar().formatmonth(year, month)

        # Month bounds (timezone-aware)
        first_day = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            last_day = timezone.make_aware(datetime(year + 1, 1, 1) - timedelta(days=1))
        else:
            last_day = timezone.make_aware(datetime(year, month + 1, 1) - timedelta(days=1))

        events = (
            Event.objects.filter(starts_at__gte=first_day, starts_at__lte=last_day)
            .select_related("circle")
        )

        # Events grouped by day
        events_by_day = {}
        for event in events:
            day = event.starts_at.day
            events_by_day.setdefault(day, []).append(event)

        # Inject events into calendar markup
        cal_with_events = str(cal)
        for day, day_events in events_by_day.items():
            day_cell = f">{day}</td>"
            event_html = '<div class="calendar-events">'
            for event in day_events:
                event_html += f'<div class="calendar-event" data-event-id="{event.id}">'
                event_html += f"<strong>{event.title}</strong><br>"
                event_html += f"<small>{event.starts_at.time()}</small>"
                event_html += "</div>"
            event_html += "</div>"
            replacement = f">{day}{event_html}</td>"
            cal_with_events = cal_with_events.replace(day_cell, replacement)

        return render(
            request,
            "circles/events_calendar.html",
            {
                "title": "Events Calendar",
                "calendar": mark_safe(cal_with_events),
                "year": year,
                "month": month,
                "prev_year": prev_year,
                "prev_month": prev_month,
                "next_year": next_year,
                "next_month": next_month,
                "events": events,
            },
        )

    except Exception as e:
        print(f"Error in events_calendar: {e}")
        return render(
            request,
            "circles/error.html",
            {"message": "An error occurred while loading the calendar."},
        )


# Placeholder views for navbar
def bulletin_board(request):
    return render(request, "circles/placeholder.html", {"title": "Bulletin Board"})


def emergency_contacts(request):
    return render(request, "circles/placeholder.html", {"title": "Emergency Contacts"})


# Circles
class CircleListView(ListView):
    model = Circle
    template_name = "circles/circle_list.html"
    context_object_name = "circles"
    paginate_by = 20
    ordering = ["name"]


class CircleDetailView(DetailView):
    model = Circle
    template_name = "circles/circle_detail.html"
    context_object_name = "circle"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["posts"] = self.object.posts.select_related("author")[:25]
        is_member = user.is_authenticated and self.object.memberships.filter(user=user).exists()
        ctx["is_member"] = is_member
        ctx["member_count"] = self.object.memberships.count()
        return ctx


class CircleCreateView(LoginRequiredMixin, CreateView):
    model = Circle
    fields = ["name", "description", "is_public"]
    template_name = "circles/circle_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("circles:circle_detail", kwargs={"slug": self.object.slug})


# Posts
class PostDetailView(DetailView):
    model = Post
    template_name = "circles/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.select_related("circle", "author").filter(
            circle__slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author")
        ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "circles/post_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.circle = get_object_or_404(Circle, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.circle = self.circle
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["circle"] = self.circle
        return ctx


# Comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "circles/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post.objects.select_related("circle"),
            pk=kwargs["pk"],
            circle__slug=kwargs["slug"],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post_obj
        form.instance.author = self.request.user
        form.save()
        return HttpResponseRedirect(self.post_obj.get_absolute_url())


# Voting
class PostVoteView(LoginRequiredMixin, View):
    def post(self, request, slug, pk, value):
        post = get_object_or_404(Post, pk=pk, circle__slug=slug)
        Vote.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={"value": int(value)},
        )
        return HttpResponseRedirect(post.get_absolute_url())


# Membership (join/leave circles)
class JoinCircleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        circle = get_object_or_404(Circle, slug=slug)
        Membership.objects.get_or_create(user=request.user, circle=circle)
        return HttpResponseRedirect(circle.get_absolute_url())


class LeaveCircleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        circle = get_object_or_404(Circle, slug=slug)
        Membership.objects.filter(user=request.user, circle=circle).delete()
        return HttpResponseRedirect(circle.get_absolute_url())


# Events CRUD
class EventListView(ListView):
    model = Event
    template_name = "circles/events_list.html"
    context_object_name = "events"
    ordering = ["starts_at"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("circle", "created_by")
        circle_slug = self.request.GET.get("circle")
        if circle_slug:
            qs = qs.filter(circle__slug=circle_slug)
        return qs


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "circles/event_form.html"
    success_url = reverse_lazy("circles:events_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "circles/event_form.html"
    success_url = reverse_lazy("circles:events_list")

    def get_queryset(self):
        # Only allow owners to edit their events
        return Event.objects.filter(created_by=self.request.user)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "circles/event_confirm_delete.html"
    success_url = reverse_lazy("circles:events_list")

    def get_queryset(self):
        # Only allow owners to delete their events
        return Event.objects.filter(created_by=self.request.user)


# Activities CRUD
class ActivityListView(ListView):
    model = Activity
    template_name = "circles/activities_list.html"
    context_object_name = "activities"
    ordering = ["day_of_week", "start_time"]


class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "circles/activities_form.html"
    success_url = reverse_lazy("circles:activities_list")


class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "circles/activities_form.html"
    success_url = reverse_lazy("circles:activities_list")


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = "circles/activity_confirm_delete.html"
    success_url = reverse_lazy("circles:activities_list")


# User Registration (Sign Up)
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("circles:index")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# Login
class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


# Search
def search(request):
    query = request.GET.get("q", "")
    results = {"circles": [], "posts": [], "activities": [], "events": []}

    if query:
        results["circles"] = Circle.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:5]

        results["posts"] = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).select_related("circle", "author")[:5]

        results["activities"] = Activity.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )[:5]

        results["events"] = Event.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        ).select_related("circle")[:5]

    return render(request, "circles/search_results.html", {"query": query, "results": results})