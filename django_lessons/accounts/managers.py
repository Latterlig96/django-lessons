from typing import Any, Dict, TypeVar

from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

_CustomUser = TypeVar("_CustomUser")


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username: str, email: str, password: str, **extra_fields: Dict[Any, Any]
    ) -> _CustomUser:
        if not email:
            raise ValueError(_("The Email must be set"))
        if not username:
            raise ValueError(_("The username must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields: Dict[Any, Any]
    ) -> _CustomUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_student", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )


class StudentManager(CustomUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_student=True)


class TutorManager(CustomUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_student=False)
