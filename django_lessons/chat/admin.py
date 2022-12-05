from django.contrib import admin

from .forms import ChatRoomForm
from .models import ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("room_name", "student")
    form = ChatRoomForm
