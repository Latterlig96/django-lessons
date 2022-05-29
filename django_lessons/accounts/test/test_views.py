from http import HTTPStatus
from typing import Any, Dict

from django.test import TestCase
from django.urls import reverse

from accounts.models import Messages, StudentUser, TutorUser


class TestStudentRegisterView(TestCase):
    def setUp(self):
        self.correct_case: Dict[str, Any] = {
            "username": "TestUser",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "email": "teststudent@gmail.com",
            "password1": "TestPassword1",
            "password2": "TestPassword1",
        }

    def test_register_student(self):
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(StudentUser.objects.filter(username="TestUser").exists())

    def test_fail_case_register_student_without_username(self):
        self.correct_case.update({"username": ""})
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(
            StudentUser.objects.filter(email="teststudent@gmail.com").exists()
        )

    def test_fail_case_register_student_without_email(self):
        self.correct_case.update({"email": ""})
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(StudentUser.objects.filter(username="TestUser").exists())

    def test_fail_case_register_student_without_first_name(self):
        self.correct_case.update({"first_name": ""})
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(StudentUser.objects.filter(username="TestUser").exists())

    def test_fail_case_register_student_without_last_name(self):
        self.correct_case.update({"last_name": ""})
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(StudentUser.objects.filter(username="TestUser").exists())

    def test_fail_case_register_student_without_non_matching_password(self):
        self.correct_case.update({"password1": ""})
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(StudentUser.objects.filter(username="TestUser").exists())


class TestStudentProfileView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )

    def test_student_profile_view(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.get(
            reverse("accounts:profile", kwargs={"pk": profile.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_fail_case_student_profile_view_wrong_pk(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.get(reverse("accounts:profile", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestStudentUserSettingsView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
        self.correct_case = {
            "username": "TestUser",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "email": "teststudent@gmail.com",
            "image": "",
            "location": "Cracow",
            "phone_number": "+48 333 333 333",
        }

    def test_student_user_settings_view(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.post(
            reverse("accounts:settings", kwargs={"pk": profile.id}), self.correct_case
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_fail_case_student_user_settings_view_without_username(self):
        self.correct_case.update({"username": ""})
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.post(
            reverse("accounts:settings", kwargs={"pk": profile.id}), self.correct_case
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/settings.html")

    def test_fail_case_student_user_settings_view_without_first_name(self):
        self.correct_case.update({"first_name": ""})
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.post(
            reverse("accounts:settings", kwargs={"pk": profile.id}), self.correct_case
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/settings.html")

    def test_fail_case_student_user_settings_view_without_last_name(self):
        self.correct_case.update({"last_name": ""})
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.post(
            reverse("accounts:settings", kwargs={"pk": profile.id}), self.correct_case
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/settings.html")


class TestMessageListView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
        TutorUser.objects.create(
            username="TestTutorUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="testtutor@gmail.com",
            password="testPassword",
            is_student=False,
        )

    def test_message_list_view_as_student(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.get(
            reverse("accounts:messages", kwargs={"pk": profile.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_message_list_view_as_(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.get(
            reverse("accounts:messages", kwargs={"pk": profile.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestMessageDetailView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
        TutorUser.objects.create(
            username="TestTutorUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="testtutor@gmail.com",
            password="testPassword",
            is_student=False,
        )
        Messages.objects.create(
            tutor_user=TutorUser.objects.get(username="TestTutorUser"),
            student_user=StudentUser.objects.get(username="TestUser"),
            title="TestTitle",
            message="TestMessage",
        )

    def test_message_detail_view(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        message = Messages.objects.get(title="TestTitle")
        response = self.client.get(
            reverse(
                "accounts:message_detail",
                kwargs={"pk": profile.id, "message_id": message.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestStudentListView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )

    def test_student_list_view(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        response = self.client.get(reverse("accounts:students"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
