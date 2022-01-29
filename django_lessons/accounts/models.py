from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager, StudentManager, TutorManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

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

    email = models.EmailField(
        _('email address'), blank=False, null=False, unique=True)
    password = models.CharField(
        _('password'), blank=False, null=False, max_length=50)
    first_name = models.CharField(
        _('first name'), max_length=150, blank=False, null=False)
    last_name = models.CharField(
        _('last name'), max_length=150, blank=False, null=False)
    is_student = models.BooleanField(_('is_student'), default=True)
    is_subscriber = models.BooleanField(default=False)

    objects = CustomUserManager()

    @property
    def has_subscription(self) -> bool:
        return self.is_subscriber

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentUser(CustomUser):

    objects = StudentManager()

    class Meta:
        proxy = True


class TutorUser(CustomUser):

    objects = TutorManager()

    class Meta:
        proxy = True


class ProfileBase(models.Model):

    image = models.ImageField(upload_to='images', null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    phone_number = PhoneNumberField(blank=True)

    class Meta:
        abstract = True


class StudentProfile(ProfileBase):

    user = models.OneToOneField(StudentUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class TutorProfile(ProfileBase):

    user = models.OneToOneField(TutorUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Messages(models.Model):

    tutor_user = models.ForeignKey(
        TutorUser, on_delete=models.CASCADE, related_name="tutor_user")
    student_user = models.ForeignKey(
        StudentUser, on_delete=models.CASCADE, related_name="student_user")
    title = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Message from {self.tutor_user} to {self.student_user}"
