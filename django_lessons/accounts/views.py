from typing import Any, Dict

from app.models import Activities, Answer
from django.contrib import messages
from django.contrib.auth import views
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import (InlineStudentProfileForm, InlineTutorProfileForm,
                    MessageForm, PasswordResetForm, SetPasswordForm,
                    StudentAccountRegisterForm, StudentLoginForm,
                    StudentProfileForm, TutorProfileForm)
from .models import (Messages, StudentProfile, StudentUser, TutorProfile,
                     TutorUser)


class StudentRegisterView(CreateView):
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
    form_class = StudentAccountRegisterForm
    success_message = _("Your profile was created successfully")

    def form_valid(self, form: StudentAccountRegisterForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class StudentProfileView(DetailView):
    template_name = "accounts/student_profile.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance, _ = StudentProfile.objects.get_or_create(user=super().get_object())
        if Activities.objects.filter(student=instance.user).exists():
            context["activities"] = Activities.objects.filter(
                student=instance.user
            ).order_by("created_at")[:10]
        context["student_profile"] = instance
        return context

    def get_queryset(self) -> QuerySet:
        return StudentUser.objects.filter(id=self.kwargs["pk"])


class StudentUserSettingsView(UpdateView):
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:profile")
    form_class = StudentProfileForm
    success_message = _("Your account has been sucessfully updated")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = StudentProfile.objects.get(user=super().get_object())
        if self.request.POST:
            context["student_profile_form"] = InlineStudentProfileForm(
                self.request.POST, self.request.FILES, instance=instance
            )
            return context
        form = InlineStudentProfileForm(
            instance=instance,
            initial={
                "image": instance.image,
                "location": instance.location,
                "phone_number": instance.phone_number,
            },
        )
        context["student_profile_form"] = form
        return context

    def get_queryset(self) -> QuerySet:
        return StudentUser.objects.filter(id=self.kwargs["pk"])

    def get_initial(self) -> Dict[str, Any]:
        self.initial.update(
            {
                "username": self.request.user.username,
                "email": self.request.user.email,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
            }
        )
        return super().get_initial()

    def form_valid(self, form: StudentProfileForm) -> HttpResponse:
        context = self.get_context_data()
        student_profile_form = context["student_profile_form"]
        if form.is_valid() and student_profile_form.is_valid():
            form.save()
            student_profile_form.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(
                reverse_lazy("accounts:profile", kwargs={"pk": self.kwargs["pk"]})
            )
        return HttpResponseRedirect(
            reverse_lazy("accounts:profile", kwargs={"pk": self.kwargs["pk"]})
        )


class TutorProfileView(DetailView):
    template_name = "accounts/tutor_profile.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance, _ = TutorProfile.objects.get_or_create(user=super().get_object())
        context["tutor_profile"] = instance
        return context

    def get_queryset(self) -> QuerySet:
        return TutorUser.objects.filter(id=self.kwargs["pk"])


class TutorUserSettingsView(UpdateView):
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:tutor_profile")
    form_class = TutorProfileForm
    success_message = _("Your account has been sucessfully updated")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = TutorProfile.objects.get(user=super().get_object())
        if self.request.POST:
            context["tutor_profile_form"] = InlineTutorProfileForm(
                self.request.POST, self.request.FILES, instance=instance
            )
            return context
        form = InlineTutorProfileForm(
            instance=instance,
            initial={
                "image": instance.image,
                "location": instance.location,
                "phone_number": instance.phone_number,
            },
        )
        context["tutor_profile_form"] = form
        return context

    def get_queryset(self) -> QuerySet:
        return TutorUser.objects.filter(id=self.kwargs["pk"])

    def get_initial(self) -> Dict[str, Any]:
        self.initial.update(
            {
                "username": self.request.user.username,
                "email": self.request.user.email,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
            }
        )
        return super().get_initial()

    def form_valid(self, form: TutorProfileForm) -> HttpResponse:
        context = self.get_context_data()
        tutor_profile_form = context["tutor_profile_form"]
        if form.is_valid() and tutor_profile_form.is_valid():
            form.save()
            tutor_profile_form.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(
                reverse_lazy("accounts:tutor_profile", kwargs={"pk": self.kwargs["pk"]})
            )
        return HttpResponseRedirect(
            reverse_lazy("accounts:tutor_profile", kwargs={"pk": self.kwargs["pk"]})
        )


class MessageListView(ListView):
    template_name = "accounts/message_list.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_tutor:
            queryset = Messages.objects.filter(tutor_user=self.kwargs["pk"]).all()
            return queryset
        queryset = Messages.objects.filter(student_user=self.kwargs["pk"]).all()
        return queryset


class MessageDetailView(DetailView):
    template_name = "accounts/message_detail.html"
    model = Messages


class MessageFormView(CreateView):
    template_name = "accounts/message_form.html"
    form_class = MessageForm

    def get_initial(self) -> Dict[str, Any]:
        student = StudentUser.objects.get(id=self.kwargs["student_id"])
        self.initial.update({"tutor_user": self.request.user, "student_user": student})
        return super().get_initial()

    def form_valid(self, form: MessageForm) -> HttpResponse:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse_lazy("accounts:tutor_profile", kwargs={"pk": self.kwargs["pk"]})
            )
        return HttpResponseRedirect(
            reverse_lazy("accounts:tutor_profile", kwargs={"pk": self.kwargs["pk"]})
        )


class StudentListView(ListView):
    template_name = "accounts/student_list.html"

    def get_queryset(self) -> QuerySet:
        return StudentProfile.objects.select_related("user").all()


class LoginView(views.LoginView):
    template_name = "accounts/login.html"
    form_class = StudentLoginForm


class LogoutView(views.LogoutView):
    pass


class PasswordResetView(views.PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    form_class = PasswordResetForm


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_form.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("accounts:login")
    success_message = _("You password has been successfully reseted")

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class PasswordChangeView(views.PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("accounts:password_change_done")


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class StudentAnswersListView(ListView):
    template_name = "accounts/student_answers.html"
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        return Answer.objects.filter(student=self.request.user.id).all()


class StudentAnswersDetailView(DetailView):
    template_name = "accounts/student_answer.html"

    def get_object(self):
        return Answer.objects.get(pk=self.kwargs["answer_pk"])
