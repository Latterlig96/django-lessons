from typing import TypeVar
from django.contrib import messages
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from .forms import PasswordResetForm, SetPasswordForm, StudentAccountRegisterForm, \
                   StudentLoginForm, StudentProfileForm, InlineStudentProfileForm
from .models import StudentUser, StudentProfile


class StudentRegisterView(CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = StudentAccountRegisterForm
    success_message = _("Your profile was created successfully")

    def form_valid(self, form: StudentAccountRegisterForm) -> TypeVar('httpResponse'):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class StudentUserProfileView(UpdateView):
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = StudentProfileForm
    success_message = _('Your account has been sucessfully updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance, _ = StudentProfile.objects.get_or_create(user=super().get_object())
        if self.request.POST:
            context['student_profile_form'] = InlineStudentProfileForm(self.request.POST, instance=instance)
            return context
        form = InlineStudentProfileForm(instance=instance,
                                        initial={'image': instance.image,
                                                'location': instance.location,
                                                'phone_number': instance.phone_number})
        context['student_profile_form'] = form
        return context
    
    def get_queryset(self):
        return StudentUser.objects.filter(id=self.kwargs['pk'])

    def get_initial(self):
        self.initial.update({'username': self.request.user.username,
                             'email': self.request.user.email,
                             'first_name': self.request.user.first_name,
                             'last_name': self.request.user.last_name})
        return super().get_initial()
    
    def form_valid(self, form: StudentProfileForm) -> TypeVar('httpResponse'):
        context = self.get_context_data()
        student_profile_form = context['student_profile_form']
        if form.is_valid() and student_profile_form.is_valid():
            form.save()
            student_profile_form.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'pk': self.kwargs['pk']}))
        return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'pk': self.kwargs['pk']}))
    
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

    def form_valid(self, form: SetPasswordForm) -> TypeVar('httpResponse'):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class PasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
