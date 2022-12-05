from accounts.models import StudentUser
from app.models import Answer, Exercise, Favorites, Module, Subject, Activities
from django.db.utils import IntegrityError
from django.test import TestCase


class TestSubject(TestCase):
    def test_subject_model(self):
        Subject.objects.create(subject="Math")
        self.assertTrue(Subject.objects.filter(subject="Math").exists())

    def test_fail_case_subject_model_without_subject(self):
        with self.assertRaises(IntegrityError) as context:
            Subject.objects.create(subject=None)
            self.assertEqual(Subject.objects.all(), 0)

    def test_fail_case_subject_model_unsupported_subject(self):
        with self.assertRaises(IntegrityError) as context:
            Subject.objects.create(subject="Physical Education")
            self.assertFalse(
                Subject.objects.filter(subject="Physical Education").exists()
            )


class TestModule(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")

    def test_module_model(self):
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="testDescription",
        )
        self.assertTrue(Module.objects.filter(title="testTitle").exists())

    def test_fail_case_module_model_empty_subject(self):
        with self.assertRaises(IntegrityError) as context:
            Module.objects.create(
                subject=None, title="testTitle", description="testDescription"
            )
            self.assertFalse(Module.objects.filter(title="testTitle").exists())


class TestExercise(TestCase):
    def setUp(self):
        Subject.objects.create(subject="Math")
        Module.objects.create(
            subject=Subject.objects.get(subject="Math"),
            title="testTitle",
            description="testDescription",
        )

    def test_exercise_model(self):
        Exercise.objects.create(
            module=Module.objects.get(title="testTitle"),
            title="testTitle",
            image_description=None,
            text_description="TestDescription",
            exercise_image_answer=None,
            exercise_text_answer="testAnswer",
        )
        self.assertTrue(Exercise.objects.filter(title="testTitle").exists())

    def test_fail_case_exercise_model_empty_module(self):
        with self.assertRaises(IntegrityError) as context:
            Exercise.objects.create(
                module=None,
                title="testTitle",
                image_description=None,
                text_description="TestDescription",
                exercise_image_answer=None,
                exercise_text_answer="testAnswer",
            )
            self.assertFalse(Exercise.objects.filter(title="testTitle").exists())


class TestAnswer(TestCase):
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
            exercise_image_answer=None,
            exercise_text_answer="TestAnswer",
        )

    def test_answer_model(self):
        Answer.objects.create(
            student=StudentUser.objects.get(username="TestUser"),
            exercise=Exercise.objects.get(title="TestTitle"),
            answer_image=None,
            answer_text="TestAnswer",
        )
        self.assertTrue(Answer.objects.filter(answer_text="TestAnswer").exists())

    def test_fail_case_asnwer_model_without_student(self):
        with self.assertRaises(IntegrityError) as context:
            Answer.objects.create(
                student=None,
                exercise=Exercise.objects.get(title="TestTitle"),
                answer_image=None,
                answer_text="TestAnswer",
            )
            self.assertFalse(Answer.objects.filter(answer_text="TestAnswer").exists())

    def test_fail_case_asnwer_model_without_exercise(self):
        with self.assertRaises(IntegrityError) as context:
            Answer.objects.create(
                student=StudentUser.objects.get(username="TestUser"),
                exercise=None,
                answer_image=None,
                answer_text="TestAnswer",
            )
            self.assertFalse(Answer.objects.filter(answer_text="TestAnswer").exists())


class TestFavorites(TestCase):
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
            exercise_image_answer=None,
            exercise_text_answer="TestAnswer",
        )

    def test_favorites_model(self):
        Favorites.objects.create(
            student=StudentUser.objects.get(username="TestUser"),
            exercise=Exercise.objects.get(title="TestTitle"),
        )
        self.assertTrue(Favorites.objects.filter(student__username="TestUser").exists())

class TestActivities(TestCase):

    def setUp(self):
        StudentUser.objects.create(
            username="TestUser",
            first_name="TestFirstName",
            last_name="TestLastName",
            email="teststudent@gmail.com",
            password="testPassword",
        )
    
    def test_create_activity(self):
        student = StudentUser.objects.get(username="TestUser")
        Activities.objects.create(
            student=student,
            description="TestActivity")
        self.assertTrue(Activities.objects.filter(student=student).exists())
    

    def test_return_monthly_activities(self):
        student = StudentUser.objects.get(username="TestUser")
        Activities.objects.create(
            student=student,
            description="TestActivity")
        monthly_activities = Activities.get_monthly_activities(student)["count"]
        self.assertEquals(monthly_activities, 2)
    
    def test_return_daily_activities(self):
        student = StudentUser.objects.get(username="TestUser")
        Activities.objects.create(
            student=student,
            description="TestActivity")
        daily_activities = Activities.get_daily_activities(student)["count"]
        self.assertEquals(daily_activities, 2)
