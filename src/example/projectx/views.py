# Create your views here.
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    The projectX homepage, that users see when they start up the application
    """
    template_name = "home.html"
