from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AsyncChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self._room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self._room_group_name = f"chat_{self._room_name}"

        await self.channel_layer.group_add(self._room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self._room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = await self.decode_json(text_data)
        await self.channel_layer.group_send(
            self._room_group_name,
            {
                "type": "chat_message",
                "user": text_data_json["user"],
                "message": text_data_json["message"],
            },
        )

    async def chat_message(self, event):
        await self.send_json(event)
