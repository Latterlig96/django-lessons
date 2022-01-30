from typing import Any, Dict, TypeVar

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import AnswerForm, FavoritesForm
from .models import Exercise, Favorites, Module, Subject

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
        if self.request.user.is_anonymous:
            return Exercise.objects.filter(module=self.kwargs['module_id'], is_premium=False)
        if not self.request.user.has_subscription:
            return Exercise.objects.filter(module=self.kwargs['module_id'], is_premium=False)
        return Exercise.objects.filter(module=self.kwargs['module_id'], is_premium=True)


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

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('app:exercises', kwargs={"module_id": self.kwargs["module_id"]}))
        return super().get(request, *args, **kwargs)

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
        queryset = Favorites.objects.select_related(
            'exercise').filter(student=self.request.user).all()
        return queryset
