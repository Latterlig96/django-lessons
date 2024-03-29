from typing import Any, Dict

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import AnswerForm, ContactForm, FavoritesForm
from .models import Activities, Exercise, Favorites, Module, Subject


class IndexView(TemplateView):
    template_name = "app/index.html"


@method_decorator(csrf_exempt, name="dispatch")
class ContactView(TemplateView, RedirectView):
    template_name = "app/contact.html"
    default_subject = "Contact from %s"

    def get_context_data(self):
        context = super().get_context_data()
        context["contact_form"] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContactForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_mail(
                self.default_subject.format(data["name"]),
                data["message"],
                data["email"],
                [settings.EMAIL_HOST_USER],
            )
            return self.render_to_response(context)
        return self.render_to_response(context)


class SubjectsListView(ListView):
    model = Subject


class ModulesListView(ListView):
    def get_queryset(self) -> QuerySet:
        queryset = Module.objects.filter(subject=self.kwargs["subject_id"])
        return queryset


class ExerciseListView(ListView):
    def get_queryset(self) -> QuerySet:
        if self.request.user.is_anonymous:
            return Exercise.objects.filter(
                module=self.kwargs["module_id"], is_premium=False
            )
        if not self.request.user.has_subscription:
            return Exercise.objects.filter(
                module=self.kwargs["module_id"], is_premium=False
            )
        return Exercise.objects.filter(module=self.kwargs["module_id"]).all()


class ExerciseDetailView(UpdateView):
    form_class = AnswerForm
    template_name = "app/exercise_detail.html"

    def get_queryset(self) -> QuerySet:
        return Exercise.objects.filter(id=self.kwargs["pk"])

    def get_initial(self) -> Dict[str, Any]:
        self.initial.update(
            {"student": self.request.user, "exercise": super().get_object()}
        )
        return super().get_initial()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["favorites_form"] = FavoritesForm(
            initial={"student": self.request.user, "exercise": super().get_object()}
        )
        return context

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        if self.request.user.is_anonymous:
            messages.info(
                self.request,
                _("Unauthenticated users can't see exercise content, please log in"),
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "app:exercises", kwargs={"module_id": self.kwargs["module_id"]}
                )
            )
        if not self.request.user.has_subscription and super().get_object().is_premium:
            messages.info(
                self.request,
                _(
                    "Users without subscription have no permissions to visit this exercise"
                ),
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "app:exercises", kwargs={"module_id": self.kwargs["module_id"]}
                )
            )
        return super().get(request, *args, **kwargs)

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        if "favorite-button" in self.request.POST:
            exercise = super().get_object()
            activities = Activities.objects.create(student=self.request.user)
            activities.description = _("Added exercise %(title)s to favorites") % {
                "title": exercise.title
            }
            activities.save()
            if Favorites.objects.filter(exercise=exercise).exists():
                return super().post(request, *args, **kwargs)
            favorites_form = FavoritesForm().save(commit=False)
            favorites_form.student = self.request.user
            favorites_form.exercise = exercise
            favorites_form.save()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: AnswerForm) -> HttpResponse:
        exercise = super().get_object()
        activities = Activities.objects.create(student=self.request.user)
        activities.description = _("Submitted answer for exercise %(title)s") % {
            "title": exercise.title
        }
        activities.save()
        answer_form = AnswerForm(self.request.POST)
        answer_form.save()
        response = super().form_valid(form)
        return response


class FavoritesListView(ListView):
    template_name = "app/favorites.html"
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        queryset = (
            Favorites.objects.select_related("exercise")
            .filter(student=self.request.user)
            .all()
        )
        return queryset
