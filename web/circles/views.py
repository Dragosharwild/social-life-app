from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Circle, Post, Activity,
    Comment, Vote, Membership
)
from .forms import PostForm, ActivityForm, CommentForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.db.models import Q


# Home
def home(request):
    return render(request, "circles/index.html")


# Placeholder views for navbar
def events_calendar(request):
    return render(request, "circles/placeholder.html", {"title": "Events Calendar"})

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
        # recent posts
        ctx["posts"] = self.object.posts.select_related("author")[:25]
        # membership info
        user = self.request.user
        is_member = False
        if user.is_authenticated:
            is_member = self.object.memberships.filter(user=user).exists()
        ctx["is_member"] = is_member
        ctx["member_count"] = self.object.memberships.count()
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('circles:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Search Functionality
def search(request):
    query = request.GET.get('q', '')
    results = {
        'circles': [],
        'posts': [],
        'activities': [],
    }
    
    if query:
        # Search Circles
        results['circles'] = Circle.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        # Search posts
        results['posts'] = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).select_related('circle', 'author')[:5]
        
        # Search Activities
        results['activities'] = Activity.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )[:5]
        
    return render(request, 'circles/search_results.html', {
        'query': query,
        'results': results
    })