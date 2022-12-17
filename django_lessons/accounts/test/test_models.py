from typing import Any, Dict

from accounts.models import (CustomUser, Messages, StudentProfile, StudentUser,
                             TutorUser, TutorProfile)
from django.db.utils import IntegrityError
from django.test import TestCase
from django.db.models.signals import post_save
from unittest.mock import patch 


class CustomUserTest(TestCase):
    def setUp(self):
        self.correct_case: Dict[str, Any] = {
            "username": "TestUser",
            "email": "testemail@gmail.com",
            "password": "TestPassword",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "is_student": False,
            "is_subscriber": False,
        }

    def test_create_user(self):
        CustomUser.objects.create(**self.correct_case)
        self.assertTrue(CustomUser.objects.filter(username="TestUser").exists())

    def test_fail_case_user_without_username(self):
        with self.assertRaises(IntegrityError) as context:
            self.correct_case.update({"username": None})
            CustomUser.objects.create(**self.correct_case)
            self.assertFalse(
                CustomUser.objects.filter(username="testemail@gmail.com").exists()
            )

    def test_fail_case_user_without_email(self):
        with self.assertRaises(IntegrityError) as context:
            self.correct_case.update({"email": None})
            CustomUser.objects.create(**self.correct_case)
            self.assertFalse(
                CustomUser.objects.filter(username="testemail@gmail.com").exists()
            )

    def test_fail_case_user_without_first_name(self):
        with self.assertRaises(IntegrityError) as context:
            self.correct_case.update({"first_name": None})
            CustomUser.objects.create(**self.correct_case)
            self.assertFalse(CustomUser.objects.filter(username="TestUser").exists())

    def test_fail_case_user_without_last_name(self):
        with self.assertRaises(IntegrityError) as context:
            self.correct_case.update({"last_name": None})
            CustomUser.objects.create(**self.correct_case)
            self.assertFalse(CustomUser.objects.filter(username="TestUser").exists())

class StudentUserTest(TestCase):
    def setUp(self):
        self.correct_case: Dict[str, Any] = {
            "username": "TestUser",
            "email": "testemail@gmail.com",
            "password": "TestPassword",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "is_student": True,
            "is_subscriber": False
        }

    def test_student_user_create(self):
        StudentUser.objects.create(**self.correct_case)
        self.assertTrue(StudentUser.objects.filter(username="TestUser").exists())

    def test_student_profile_created_on_student_user_creation(self):
        with patch("accounts.signals.create_student_profile_signal", autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=StudentUser, dispatch_uid="test_mock")
        StudentUser.objects.create(**self.correct_case)
        self.assertTrue(StudentUser.objects.filter(username="TestUser").exists())
        self.assertEquals(mocked_handler.call_count, 1)

class TutorUserTest(TestCase):
    def setUp(self):
        self.correct_case: Dict[str, Any] = {
            "username": "TestUser",
            "email": "testemail@gmail.com",
            "password": "TestPassword",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "is_student": False,
            "is_subscriber": False
        }

    def test_student_user_create(self):
        TutorUser.objects.create(**self.correct_case)
        self.assertTrue(TutorUser.objects.filter(username="TestUser").exists())

    def test_tutor_profile_created_on_tutor_user_creation(self):
        with patch("accounts.signals.create_tutor_profile_signal", autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=TutorUser, dispatch_uid="test_mock")
        TutorUser.objects.create(**self.correct_case)
        self.assertTrue(TutorUser.objects.filter(username="TestUser").exists())
        self.assertEquals(mocked_handler.call_count, 1)

class StudentProfileTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username="TestUser",
            email="testemail@gmail.com",
            first_name="testFirstName",
            last_name="testLastName",
            is_student=True,
        )
        self.correct_case: Dict[str, Any] = {
            "user": CustomUser.objects.get(username="TestUser"),
            "image": None,
            "location": "TestLocation",
            "phone_number": "333-333-333",
        }

    def test_create_student_profile(self):
        StudentProfile.objects.create(**self.correct_case)
        self.assertTrue(
            StudentProfile.objects.filter(user__username="TestUser").exists()
        )


class TutorProfileTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username="TestUser",
            email="testemail@gmail.com",
            first_name="testFirstName",
            last_name="testLastName",
            is_student=False,
        )
        self.correct_case: Dict[str, Any] = {
            "user": CustomUser.objects.get(username="TestUser"),
            "image": None,
            "location": "TestLocation",
            "phone_number": "333-333-333",
        }

    def test_create_student_profile(self):
        TutorProfile.objects.create(**self.correct_case)
        self.assertTrue(
            TutorProfile.objects.filter(user__username="TestUser").exists()
        )

class MessagesTest(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )
        TutorUser.objects.create(
            username="TestTutor",
            email="testtutor@gmail.com",
            first_name="testTutorFirstName",
            last_name="testTutorLastName",
            is_student=False,
        )

    def test_create_message(self):
        Messages.objects.create(
            tutor_user=TutorUser.objects.get(username="TestTutor"),
            student_user=StudentUser.objects.get(username="TestStudent"),
            title="TestTitle",
            message="TestMessage",
        )
        self.assertTrue(
            Messages.objects.filter(tutor_user__username="TestTutor").exists()
        )
