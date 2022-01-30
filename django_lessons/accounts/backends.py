from typing import Any, Dict, Optional, TypeVar
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    pass


class UsernameBackend(ModelBackend):
    def authenticate(self,
                     request: TypeVar('httpRequest'),
                     username: Optional[str]=None,
                     password: str=None,
                     **kwargs: Dict[Any, Any]) -> Optional[TypeVar('User')]:
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
