from accounts.models import StudentUser
from chat.forms import ChatRoomForm
from django.test import TestCase


class ChatRoomFormTest(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )
        self.correct_case = {
            "student": StudentUser.objects.get(username="TestStudent"),
            "room_name": "TestRoom",
        }

    def test_room_create_from_form(self):
        form = ChatRoomForm(data=self.correct_case)
        self.assertTrue(form.is_valid())

    def test_room_create_without_student(self):
        self.correct_case.pop("student")
        form = ChatRoomForm(data=self.correct_case)
        self.assertFalse(form.is_valid())

    def test_room_create_without_room_name(self):
        self.correct_case.pop("room_name")
        form = ChatRoomForm(data=self.correct_case)
        self.assertFalse(form.is_valid())
