from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Module, Subject, Exercise, Favorites
from .forms import AnswerForm, FavoritesForm
from typing import TypeVar, Dict, Any

_Queryset = TypeVar('_Queryset')
_HttpResponse = TypeVar('_HttpResponse')

class IndexView(TemplateView):
    template_name = 'app/index.html'

class ContactView(TemplateView):
    template_name = 'app/contact.html'

class SubjectsListView(ListView):
    model = Subject

class ModulesListView(ListView):
    
    def get_queryset(self) -> _Queryset:
        queryset = Module.objects.filter(subject=self.kwargs['subject_id'])
        return queryset

class ExerciseListView(ListView):

    def get_queryset(self) -> _Queryset:
        queryset = Exercise.objects.filter(module=self.kwargs['module_id'])
        return queryset

class ExerciseDetailView(UpdateView):
    form_class = AnswerForm
    template_name = 'app/exercise_detail.html'

    def get_queryset(self) -> _Queryset:
        if self.request.user.has_subscription:
            return Exercise.objects.all()
        return Exercise.objects.filter(is_premium=False).all()

    def get_initial(self) -> Dict[str, Any]:
        self.initial.update({'student': self.request.user,
                             'exercise': super().get_object()})
        return super().get_initial()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['favorites_form'] = FavoritesForm(initial={'student': self.request.user,
                                                           'exercise': super().get_object()})
        return context

    def post(self, request, *args, **kwargs) -> _HttpResponse:
        if 'favorite-button' in self.request.POST:
            if Favorites.objects.filter(exercise=super().get_object()).exists():
                return super().post(request, *args, **kwargs)
            favorites_form = FavoritesForm().save(commit=False)
            favorites_form.student = self.request.user
            favorites_form.exercise = super().get_object()
            favorites_form.save()
        return super().post(request, *args, **kwargs)
    
class FavoritesListView(ListView):
    template_name = 'app/favorites.html'
    paginate_by = 5

    def get_queryset(self) -> _Queryset:
        queryset = Favorites.objects.select_related('exercise').filter(student=self.request.user).all()
        return queryset
