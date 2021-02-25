from django.views.generic import ListView
from .models import Project
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Project
    template_name = 'home/index.html'
