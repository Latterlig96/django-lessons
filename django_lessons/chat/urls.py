from django.urls import path
from django.conf.urls import url

from . import views
from . import consumers

app_name = "chat"

urlpatterns = [
    path("rooms/", views.ChatRoomListView.as_view(), name="rooms"),
    path("room/create/", views.ChatRoomCreateView.as_view(), name="room_create"),
    path("room/student/<int:pk>", views.StudentChatRoomView.as_view(), name="student_chat_room"),
    path("room/<int:pk>/<str:room_name>", views.ChatRoomView.as_view(), name="chat_room")
]

websocket_url_patterns = [
    path("ws/chat/<str:room_name>", consumers.AsyncChatRoomConsumer.as_asgi())
]
