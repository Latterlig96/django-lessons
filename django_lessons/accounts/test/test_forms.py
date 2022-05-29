from typing import Any, Dict

from django.test import TestCase

from accounts.forms import StudentAccountRegisterForm


class TestStudentAccountRegisterForm(TestCase):
    def setUp(self):
        self.correct_case: Dict[str, Any] = {
            "password1": "TestPassword",
            "password2": "TestPassword",
            "username": "TestUser",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "email": "testemail@gmail.com",
        }

    def test_form_valid(self):
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_fail_case_without_username(self):
        self.correct_case.update({"username": ""})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_username_as_none(self):
        self.correct_case.update({"username": None})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_without_first_name(self):
        self.correct_case.update({"first_name": ""})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_first_name_as_none(self):
        self.correct_case.update({"first_name": None})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_without_last_name(self):
        self.correct_case.update({"last_name": ""})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_last_name_as_none(self):
        self.correct_case.update({"last_name": None})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_without_email(self):
        self.correct_case.update({"email": ""})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_email_as_none(self):
        self.correct_case.update({"email": None})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_non_matching_password(self):
        self.correct_case.update({"password1": "PleaseFail"})
        form = StudentAccountRegisterForm(data=self.correct_case)
        self.assertFalse(form.is_valid())
