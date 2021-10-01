from django import forms
from django.forms import ModelForm
from django.forms.widgets import Input
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from .models import StudentUser, TutorUser


class StudentAccountForm(ModelForm):

    class Meta:
        model = StudentUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={
                                                   'id': 'inputPassword',
                                                   'class': 'form-control',
                                                   'placeholder': 'Password',
                                                   'type': 'password'}),
            'email': Input(attrs={
                            'id': 'inputEmail',
                            'class': 'form-control',
                            'placeholder': 'Email address',
                            'type': 'email'}),
            'username': Input(attrs={
                        'id': 'inputUsername',
                        'class': 'form-control',
                        'placeholder': 'Username',
                        'type': 'username'}),
            'first_name': Input(attrs={
                            'id': 'inputFirstName',
                            'class': 'form-control',
                            'placeholder': 'First name',
                            'type': 'first_name'}),
            'last_name':  Input(attrs={
                            'id': 'inputLastName',
                            'class': 'form-control',
                            'placeholder': 'Last name',
                            'type': 'last_name'}),
        }

class StudentLoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'id': 'inputEmail',
                                                           'class': 'form-control',
                                                           'placeholder': 'Email address',
                                                           'type': 'email'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'id': 'inputPassword',
                                          'class': 'form-control',
                                          'placeholder': 'Password',
                                          'type': 'password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

class PasswordResetForm(PasswordResetForm):
    
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'id': 'inputEmail',
                                       'class': 'form-control',
                                       'placeholder': 'Email address',
                                       'type': 'email'})
    )

class SetPasswordForm(SetPasswordForm):

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
                                        'id': 'inputPassword',
                                        'class': 'form-control',
                                        'placeholder': 'Password',
                                        'type': 'password'}),
        strip=False,
    )

    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
                                        'id': 'inputPassword',
                                        'class': 'form-control',
                                        'placeholder': 'Confirm password',
                                        'type': 'password'}),
    )

class TutorAccountForm(ModelForm):

    class Meta:
        model = TutorUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={
                                                   'id': 'inputPassword',
                                                   'class': 'form-control',
                                                   'placeholder': 'Password',
                                                   'type': 'password'}),
            'email': Input(attrs={
                            'id': 'inputEmail',
                            'class': 'form-control',
                            'placeholder': 'Email address',
                            'type': 'email'}),
            'username': Input(attrs={
                        'id': 'inputUsername',
                        'class': 'form-control',
                        'placeholder': 'Username',
                        'type': 'username'}),
            'first_name': Input(attrs={
                            'id': 'inputFirstName',
                            'class': 'form-control',
                            'placeholder': 'first name',
                            'type': 'first_name'}),
            'last_name':  Input(attrs={
                            'id': 'inputLastName',
                            'class': 'form-control',
                            'placeholder': 'last name',
                            'type': 'last_name'}),
        }
