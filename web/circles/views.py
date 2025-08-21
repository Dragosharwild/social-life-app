from django.views.generic import ListView, DetailView
from .models import Circle

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