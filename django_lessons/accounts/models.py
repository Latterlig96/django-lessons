from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager, StudentManager, TutorManager


class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "first_name", "last_name"]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")}
    )

    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(blank=False, null=False, max_length=50)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )
    is_student = models.BooleanField(default=True)
    is_subscriber = models.BooleanField(default=False)

    objects = CustomUserManager()

    @property
    def has_subscription(self) -> bool:
        return self.is_subscriber

    @property
    def is_tutor(self) -> bool:
        return True if not self.is_student else False

    def __str__(self) -> str:
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

    image = models.ImageField(_("image"), upload_to="images", null=True, blank=True)
    location = models.CharField(_("location"), max_length=30, null=True, blank=True)
    phone_number = PhoneNumberField(_("phone number"), null=True, blank=True)

    class Meta:
        abstract = True


class StudentProfile(ProfileBase):

    user = models.OneToOneField(StudentUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username



class TutorProfile(ProfileBase):

    user = models.OneToOneField(TutorUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Messages(models.Model):

    tutor_user = models.ForeignKey(
        TutorUser, on_delete=models.CASCADE, related_name="tutor_user"
    )
    student_user = models.ForeignKey(
        StudentUser, on_delete=models.CASCADE, related_name="student_user"
    )
    title = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Message from {self.tutor_user} to {self.student_user}"
