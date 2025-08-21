from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Circle, Post, Activity
from .forms import PostForm, ActivityForm


# Home
def home(request):
    return render(request, "circles/index.html")


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
        ctx["posts"] = self.object.posts.select_related("author")[:25]
        return ctx


# Posts
class PostDetailView(DetailView):
    model = Post
    template_name = "circles/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.select_related("circle", "author").filter(
            circle__slug=self.kwargs["slug"]
        )


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


# Activities CRUD
class ActivityListView(ListView):
    model = Activity
    template_name = "circles/activities_list.html"
    context_object_name = "activities"
    ordering = ["day_of_week", "start_time"]


class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "circles/activity_form.html"
    success_url = reverse_lazy("circles:activities_list")


class ActivityUpdateView(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "circles/activity_form.html"
    success_url = reverse_lazy("circles:activities_list")


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = "circles/activity_confirm_delete.html"
    success_url = reverse_lazy("circles:activities_list")