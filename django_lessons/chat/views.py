from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import ChatRoom
from .forms import ChatRoomForm



@method_decorator(login_required, name="dispatch")
class ChatRoomView(DetailView):
    model = ChatRoom
    template_name = "chat/chat_room.html"
    

class ChatRoomListView(ListView):
    template_name = "chat/chat_list.html"
    
    def get_queryset(self):
        return ChatRoom.objects.all()

class ChatRoomCreateView(CreateView):
    form_class = ChatRoomForm
    template_name = "chat/chat_room_create.html"
    success_url = reverse_lazy("chat:room")

class StudentChatRoomView(ListView):
    template_name = "chat/chat_list.html"
    
    def get_queryset(self):
        return ChatRoom.objects.filter(student = self.request.user)
