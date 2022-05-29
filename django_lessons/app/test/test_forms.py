from django.test import TestCase

from accounts.models import StudentUser
from app.forms import AnswerForm, ExerciseForm, ModuleForm, SubjectForm
from app.models import Exercise, Module, Subject


class TestSubjectForm(TestCase):
    def setUp(self):
        self.correct_case = {"subject": "Math"}

    def test_subject_form(self):
        form = SubjectForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_fail_case_subject_form_invalid_subject(self):
        self.correct_case.update({"subject": "Unknown"})
        form = SubjectForm(data=self.correct_case)
        self.assertFalse(form.is_valid())


class TestModuleForm(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")
        self.correct_case = {
            "subject": Subject.objects.get(subject="Math"),
            "title": "TestTitle",
            "description": "TestDescription",
        }

    def test_module_form(self):
        form = ModuleForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_fail_case_module_form_without_subject(self):
        self.correct_case.update({"subject": ""})
        form = ModuleForm(data=self.correct_case)
        self.assertFalse(form.is_valid())


class TestExerciseForm(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="TestDescription",
        )
        self.correct_case = {
            "module": Module.objects.get(title="testTitle"),
            "title": "TestTitle",
            "image_description": None,
            "text_description": "TestDescription",
            "image_answer": None,
            "text_answer": "TestAnswer",
        }

    def test_exercise_form(self):
        form = ExerciseForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_fail_exercise_form_without_module(self):
        self.correct_case.update({"module": ""})
        form = ExerciseForm(data=self.correct_case)
        self.assertFalse(form.is_valid())


class TestAnswerForm(TestCase):
    def setUp(self):
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
            image_description=None,
            text_description="TestDescription",
            image_answer=None,
            text_answer="TestAnswer",
        )
        self.correct_case = {
            "student": StudentUser.objects.get(username="TestUser"),
            "exercise": Exercise.objects.get(title="TestTitle"),
            "image_answer": None,
            "text_answer": "TestAnswer",
        }

    def test_answer_form(self):
        form = AnswerForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_fail_case_answer_form_without_student(self):
        self.correct_case.update({"student": ""})
        form = AnswerForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_fail_case_answer_form_without_exercise(self):
        self.correct_case.update({"exercise": ""})
        form = AnswerForm(data=self.correct_case)
        self.assertFalse(form.is_valid())
