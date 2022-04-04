from typing import Any, Dict, Optional, TypeVar

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from .models import CustomUser


class EmailBackend(ModelBackend):
    pass


class UsernameBackend(ModelBackend):
    def authenticate(self,
                     request: HttpRequest,
                     username: Optional[str]=None,
                     password: str=None,
                     **kwargs: Dict[Any, Any]) -> Optional[CustomUser]:
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
