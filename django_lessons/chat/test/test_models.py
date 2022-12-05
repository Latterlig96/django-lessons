from accounts.models import StudentUser
from chat.models import ChatRoom
from django.db.utils import IntegrityError
from django.test import TestCase


class ChatRoomTest(TestCase):
    def setUp(self):
        StudentUser.objects.create(
            username="TestStudent",
            email="teststudent@gmail.com",
            first_name="testStudentFirstName",
            last_name="testStudentLastName",
            is_student=True,
        )

    def test_chat_room_create(self):
        ChatRoom.objects.create(
            room_name="TestRoom",
            student=StudentUser.objects.get(username="TestStudent"),
        )
        self.assertTrue(ChatRoom.objects.filter(room_name="TestRoom").exists())

    def test_unique_chat_room_create(self):
        ChatRoom.objects.create(
            room_name="TestRoom",
            student=StudentUser.objects.get(username="TestStudent"),
        )
        with self.assertRaises(IntegrityError):
            ChatRoom.objects.create(
                room_name="TestRoom",
                student=StudentUser.objects.get(username="TestStudent"),
            )
            self.assertTrue(ChatRoom.objects.filter(room_name="TestRoom").count() == 1)
