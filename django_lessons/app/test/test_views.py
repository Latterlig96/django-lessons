from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import StudentUser
from app.models import Exercise, Module, Subject


class TestIndexView(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestContactView(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("app:contact"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestSubjectListView(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")

    def test_subject_list_view(self):
        response = self.client.get(reverse("app:subjects"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestModuleListView(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="testDescription",
        )

    def test_module_list_view(self):
        subject = Subject.objects.get(subject="Math")
        response = self.client.get(
            reverse("app:modules", kwargs={"subject_id": subject.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestExerciseListView(TestCase):
    def setUp(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )

        file = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")

        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="testDescription",
        )
        Exercise.objects.create(
            module=Module.objects.get(title="testTitle"),
            title="testTitle",
            image_description=file,
            text_description="TestDescription",
            exercise_image_answer=None,
            exercise_text_answer="testAnswer",
        )

    def test_exercise_list_view(self):
        module = Module.objects.get(title="testTitle")
        response = self.client.get(
            reverse("app:exercises", kwargs={"module_id": module.id})
        )
        self.assertTrue(response.status_code, HTTPStatus.OK)


class TestExerciseDetailView(TestCase):
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
            is_subscriber=True,
        )
        StudentUser.objects.create(
            username="TestUserWithoutSubscription",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudentwithoutsubscription@gmail.com",
            password="testPassword",
            is_subscriber=False,
        )
        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="testDescription",
        )
        Exercise.objects.create(
            module=Module.objects.get(title="testTitle"),
            title="testTitle",
            image_description=file,
            text_description="TestDescription",
            exercise_image_answer=None,
            exercise_text_answer="testAnswer",
        )
        self.answer_form = {
            "student": StudentUser.objects.get(username="TestUser"),
            "exercise": Exercise.objects.get(title="testTitle"),
            "answer_image": "",
            "answer_text": "SimpleTextAnswer",
        }

    def test_exercise_detail_view(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        exercise = Exercise.objects.get(title="testTitle")
        module = Module.objects.get(title="testTitle")
        response = self.client.get(
            reverse("app:exercise", kwargs={"module_id": module.id, "pk": exercise.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_exercise_detail_view_student_without_subscription(self):
        profile = StudentUser.objects.get(username="TestUserWithoutSubscription")
        self.client.force_login(user=profile)
        exercise = Exercise.objects.get(title="testTitle")
        module = Module.objects.get(title="testTitle")
        response = self.client.get(
            reverse("app:exercise", kwargs={"module_id": module.id, "pk": exercise.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_exercise_detail_view_post(self):
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        exercise = Exercise.objects.get(title="testTitle")
        module = Module.objects.get(title="testTitle")
        response = self.client.post(
            reverse("app:exercise", kwargs={"module_id": module.id, "pk": exercise.id}),
            data=self.answer_form,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_exercise_detail_view_post_without_student(self):
        self.answer_form.update({"student": ""})
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        exercise = Exercise.objects.get(title="testTitle")
        module = Module.objects.get(title="testTitle")
        response = self.client.post(
            reverse("app:exercise", kwargs={"module_id": module.id, "pk": exercise.id}),
            data=self.answer_form,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_exercise_detail_view_post_without_excersise(self):
        self.answer_form.update({"exercise": ""})
        profile = StudentUser.objects.get(username="TestUser")
        self.client.force_login(user=profile)
        exercise = Exercise.objects.get(title="testTitle")
        module = Module.objects.get(title="testTitle")
        response = self.client.post(
            reverse("app:exercise", kwargs={"module_id": module.id, "pk": exercise.id}),
            data=self.answer_form,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
