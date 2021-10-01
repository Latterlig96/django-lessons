from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    password = models.CharField(_('password'), blank=False, null=False, max_length=50)
    first_name = models.CharField(_('first name'), max_length=150, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=False)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentUser(CustomUser):
    class Meta:
        proxy = True

class TutorUser(CustomUser):
    class Meta:
        proxy = True
