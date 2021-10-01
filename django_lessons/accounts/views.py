from django.contrib.auth import views
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import StudentAccountForm, StudentLoginForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from typing import TypeVar

httpResponse = TypeVar('httpResponse')

class StudentRegisterView(CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = StudentAccountForm
    success_message = _("Your profile was created successfully")

    def form_valid(self, form: StudentAccountForm) -> httpResponse:
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    form_class = StudentLoginForm

class LogoutView(views.LogoutView):
    pass

class PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = PasswordResetForm

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_form.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('accounts:login')
    success_message = _('You password has been successfully reseted')

    def form_valid(self, form: SetPasswordForm) -> httpResponse:
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
