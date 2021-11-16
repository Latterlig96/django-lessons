from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Module, Subject, Exercise


class IndexView(TemplateView):
    template_name = 'app/index.html'

class ContactView(TemplateView):
    template_name = 'app/contact.html'

class SubjectsListView(ListView):
    model = Subject

class ModulesListView(ListView):
    
    def get_queryset(self):
        queryset = Module.objects.filter(subject=self.kwargs['subject_id'])
        return queryset

class ExerciseListView(ListView):

    def get_queryset(self):
        queryset = Exercise.objects.filter(module=self.kwargs['module_id'])
        return queryset

class ExerciseDetailView(DetailView):
    model = Exercise
