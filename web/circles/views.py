from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect

from .models import Circle, Post, Activity, Comment, Vote
from .forms import PostForm, ActivityForm, CommentForm

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author")
        ctx["comment_form"] = CommentForm()
        return ctx

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "circles/comment_form.html"  # not used; we post from post_detail

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post.objects.select_related("circle"), pk=kwargs["pk"], circle__slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post_obj
        form.instance.author = self.request.user
        form.save()
        return redirect("circles:post_detail", slug=self.post_obj.circle.slug, pk=self.post_obj.pk)

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

class PostVoteView(LoginRequiredMixin, View):
    def post(self, request, slug, pk, value):
        post = get_object_or_404(Post, pk=pk, circle__slug=slug)
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={"value": value},
        )
        return HttpResponseRedirect(post.get_absolute_url())

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