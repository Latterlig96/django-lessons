from django.test import TestCase

from unittest.mock import MagicMock
from accounts.managers import CustomUserManager
from django.contrib.auth.models import User


class TestCustomUserManager(TestCase):

    def setUp(self):
        self.user_case = {
            "username": "TestUser",
            "email": "test_user@gmail.com",
            "password": "TestPassword"
        }
        self.super_user_case = {
            "username": "TestUser",
            "email": "test_user@gmail.com",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "password": "TestPassword"
        }


    def test_create_user(self):
        manager = CustomUserManager()
        manager.create_user = MagicMock(return_value=User())
        manager.create_user(**self.user_case)
        manager.create_user.assert_called_once_with(**self.user_case)
    
    def test_create_user_without_username(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.user_case.pop("username")
            manager.create_user(**self.user_case)

    def test_create_user_without_email(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.user_case.pop("email")
            manager.create_user(**self.user_case)

    def test_create_user_without_password(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.user_case.pop("password")
            manager.create_user(**self.user_case)

    def test_create_user_with_none_username(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(ValueError):
            self.user_case.update({"username": None})
            manager.create_user(**self.user_case)

    def test_create_user_with_none_email(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(ValueError):
            self.user_case.update({"email": None})
            manager.create_user(**self.user_case)   

    def test_create_user_with_none_password(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.user_case.update({"password": None})
            manager.create_user(**self.user_case)

    def test_create_super_user(self):
        manager = CustomUserManager()
        manager.create_superuser = MagicMock(return_value=User())
        manager.create_superuser(**self.super_user_case)
        manager.create_superuser.assert_called_once_with(**self.super_user_case)
    
    def test_create_super_user_without_username(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.super_user_case.pop("username")
            manager.create_superuser(**self.super_user_case)

    def test_create_super_user_without_email(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.super_user_case.pop("email")
            manager.create_superuser(**self.super_user_case)

    def test_create_super_user_without_password(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.super_user_case.pop("password")
            manager.create_superuser(**self.super_user_case)

    def test_create_super_user_without_first_name(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.super_user_case.pop("first_name")
            manager.create_superuser(**self.super_user_case)
    
    def test_create_super_user_without_last_name(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(TypeError):
            self.super_user_case.pop("last_name")
            manager.create_superuser(**self.super_user_case)

    def test_create_super_user_with_wrong_staff_field(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(ValueError):
            self.super_user_case.update({"is_staff": False})
            manager.create_superuser(**self.super_user_case)

    def test_create_super_user_with_wrong_superuser_field(self):
        manager = CustomUserManager()
        manager.create = MagicMock(return_value=User())
        with self.assertRaises(ValueError):
            self.super_user_case.update({"is_superuser": False})
            manager.create_superuser(**self.super_user_case)
