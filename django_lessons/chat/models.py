from django.db import models
from accounts.models import StudentUser


class ChatRoom(models.Model): 
    
    room_name = models.CharField(max_length=100, blank=False, null=False)
    student = models.OneToOneField(StudentUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Room: {self.room_name}"
