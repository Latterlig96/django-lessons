from django.contrib import admin
from .models import ChatRoom
from .forms import ChatRoomForm


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("room_name", "student")
    form = ChatRoomForm
