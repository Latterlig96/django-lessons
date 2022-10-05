from typing import Any, Dict

from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import CustomUser, Messages, StudentProfile, StudentUser, TutorUser


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
        StudentProfile.objects.create(**self.correct_case)
        self.assertTrue(
            StudentProfile.objects.filter(user__username="TestUser").exists()
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
