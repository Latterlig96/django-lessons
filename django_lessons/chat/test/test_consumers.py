from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.test import TestCase, override_settings



@override_settings(CHANNEL_LAYERS=settings.CHANNEL_LAYERS["test"])
class ChatRoomConsumerTest(TestCase):
    def setUp(self):
        self.correct_message = {
            "type": "chat_message",
            "user": "TestUser",
            "message": "TestMessage",
        }

    class TestAsyncConsumer(AsyncJsonWebsocketConsumer):
        def __init__(self):
            self._room_group_name = "TestGroup"
            super().__init__()

        async def receive_json(self, content):
            await self.channel_layer.group_send(
                self._room_group_name,
                {
                    "type": "chat_message",
                    "channel": content["channel"],
                    "user": content["user"],
                    "message": content["message"],
                },
            )

        async def chat_message(self, event, **kwargs):
            await self.send_json(event)

    async def test_consumer_response(self):
        communicator = WebsocketCommunicator(self.TestAsyncConsumer(), "/testws/")
        connected, _ = await communicator.connect()
        self.assert_(connected)
        await communicator.send_input(self.correct_message)
        data = await communicator.receive_json_from()
        self.assertEquals(self.correct_message, data)
