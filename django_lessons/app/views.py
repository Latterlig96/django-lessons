from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Module


class IndexView(TemplateView):
    template_name = 'app/index.html'

class ContactView(TemplateView):
    template_name = 'app/contact.html'

class ModulesView(ListView):
    model = Module
