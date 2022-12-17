from http import HTTPStatus
from typing import Any, Dict

from accounts.models import Messages, StudentUser, TutorUser
from app.models import Answer, Exercise, Module, Subject
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.db.models.signals import post_save
from unittest.mock import patch 


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

    def test_signal_triggered_on_student_register(self):
        with patch("accounts.signals.create_student_profile_signal", autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=StudentUser, dispatch_uid="test_mock")
        response = self.client.post(reverse("accounts:register"), self.correct_case)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(StudentUser.objects.filter(username="TestUser").exists())
        self.assertEquals(mocked_handler.call_count, 1)

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


class TestStudentAnswersListView(TestCase):
    def setUp(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        file = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="TestDescription",
        )
        Exercise.objects.create(
            module=Module.objects.get(title="testTitle"),
            title="TestTitle",
            image_description=file,
            text_description="TestDescription",
            exercise_image_answer=None,
            exercise_text_answer="TestAnswer",
        )
        Answer.objects.create(
            student=StudentUser.objects.get(username="TestUser"),
            exercise=Exercise.objects.get(title="TestTitle"),
            answer_image=None,
            answer_text="TestAnswer",
        )

    def test_get_exercise_detail(self):
        profile = StudentUser.objects.get(username="TestUser")
        answer = Answer.objects.get(answer_text="TestAnswer")
        self.client.force_login(user=profile)
        response = self.client.get(
            reverse(
                "accounts:student_answer_detail",
                kwargs={"pk": profile.id, "answer_pk": answer.id},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/student_answer.html")


class TestPasswordResetView(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )

    def test_password_reset_view(self):
        response = self.client.get(reverse("accounts:password_reset"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/password_reset.html")

    def test_password_reset_process(self):
        response = self.client.post(reverse("accounts:password_reset"), data={"email": "teststudent@gmail.com"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Password reset on testserver")
        token = response.context[0]["token"]
        uid = response.context[0]["uid"]
        response = self.client.get(reverse("accounts:password_reset_confirm", kwargs={"token": token, "uidb64": uid}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(reverse("accounts:password_reset_confirm", kwargs={"token": token, "uidb64": uid}), {"new_password1": "pass", "new_password2": "pass"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
