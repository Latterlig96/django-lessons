from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm,
                                       UsernameField)
from django.forms import ModelForm
from django.forms.widgets import Input, FileInput
from django.utils.translation import ugettext_lazy as _
from .models import StudentProfile, StudentUser, TutorUser, TutorProfile, Messages


class StudentAccountRegisterForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'inputPassword',
            'class': 'form-control',
            'placeholder': _('Password'),
            'type': 'password'}),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'id': 'inputPassword',
            'class': 'form-control',
            'placeholder': _('Password'),
            'type': 'password'}),
        strip=False,
    )

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    class Meta:
        model = StudentUser
        fields = ('username', 'first_name', 'last_name', 'email')
        required = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'email': Input(attrs={
                'id': 'inputEmail',
                'class': 'form-control',
                'placeholder': _('Email address'),
                'type': 'email'}),
            'username': Input(attrs={
                'id': 'inputUsername',
                'class': 'form-control',
                'placeholder': _('Username'),
                'type': 'username'}),
            'first_name': Input(attrs={
                'id': 'inputFirstName',
                'class': 'form-control',
                'placeholder': _('First name'),
                'type': 'first_name'}),
            'last_name':  Input(attrs={
                'id': 'inputLastName',
                'class': 'form-control',
                'placeholder': _('Last name'),
                'type': 'last_name'}),
        }


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentUser
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = ('password', 'is_student')


class InlineStudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ('image', 'location', 'phone_number')

        widgets = {
            'image':  FileInput(attrs={
                            'id': 'inputImage',
                            'class': 'form-control',
                            'placeholder': _('image'),
                            'type': 'file'}),
            'location':  Input(attrs={
                'id': 'inputLocation',
                'class': 'form-control',
                'placeholder': _('location'),
                'type': 'location'}),
            'phone_number':  Input(attrs={
                'id': 'inputPhoneNumber',
                'class': 'form-control',
                'placeholder': _('phone_number'),
                'type': 'phone_number'}),
        }

class TutorProfileForm(forms.ModelForm):

    class Meta:
        model = TutorUser
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = ('password', 'is_student')

class InlineTutorProfileForm(forms.ModelForm):

    class Meta:
        model = TutorProfile
        fields = ('image', 'location', 'phone_number')

        widgets = {
            'image':  FileInput(attrs={
                            'id': 'inputImage',
                            'class': 'form-control',
                            'placeholder': _('image'),
                            'type': 'file'}),
            'location':  Input(attrs={
                'id': 'inputLocation',
                'class': 'form-control',
                'placeholder': _('location'),
                'type': 'location'}),
            'phone_number':  Input(attrs={
                'id': 'inputPhoneNumber',
                'class': 'form-control',
                'placeholder': _('phone_number'),
                'type': 'phone_number'}),
        }

class StudentLoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'id': 'inputEmail',
                                                           'class': 'form-control',
                                                           'placeholder': _('Email address'),
                                                           'type': 'email'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'id': 'inputPassword',
                                          'class': 'form-control',
                                          'placeholder': _('Password'),
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
                                       'placeholder': _('Email address'),
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
            'placeholder': _('Password'),
            'type': 'password'}),
        strip=False,
    )

    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'inputPassword',
            'class': 'form-control',
            'placeholder': _('Confirm password'),
            'type': 'password'}),
    )


class TutorAccountForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_student'].initial = False

    class Meta:
        model = TutorUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        required = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={
                'id': 'inputPassword',
                'class': 'form-control',
                'placeholder': _('Password'),
                'type': 'password'}),
            'email': Input(attrs={
                'id': 'inputEmail',
                'class': 'form-control',
                'placeholder': _('Email address'),
                'type': 'email'}),
            'username': Input(attrs={
                'id': 'inputUsername',
                'class': 'form-control',
                'placeholder': _('Username'),
                'type': 'username'}),
            'first_name': Input(attrs={
                'id': 'inputFirstName',
                'class': 'form-control',
                'placeholder': _('first name'),
                'type': 'first_name'}),
            'last_name':  Input(attrs={
                'id': 'inputLastName',
                'class': 'form-control',
                'placeholder': _('last name'),
                'type': 'last_name'}),
        }

class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tutor_user'].widget = forms.HiddenInput()
        self.fields['student_user'].widget = forms.HiddenInput()

    class Meta:
        model = Messages
        fields = '__all__'
