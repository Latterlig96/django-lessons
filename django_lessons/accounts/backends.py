from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from typing import TypeVar, Optional, Dict, Any

httpRequest = TypeVar('httpRequest')

class EmailBackend(ModelBackend):
    pass 

class UsernameBackend(ModelBackend):
    def authenticate(self, 
                     request: httpRequest, 
                     username: Optional[str]=None, 
                     password: str=None, 
                     **kwargs: Dict[Any, Any]):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
