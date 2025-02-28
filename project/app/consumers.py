import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, FanRegister, PublisherRegister
from django.utils.timezone import now

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"chat_{self.scope['url_route']['kwargs']['event_id']}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        fan_id = data["fan_id"]
        publisher_id = data["publisher_id"]

        fan = FanRegister.objects.get(id=fan_id)
        publisher = PublisherRegister.objects.get(id=publisher_id)
        ChatMessage.objects.create(fan=fan, publisher=publisher, message=message, timestamp=now())

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "fan": fan.name}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "fan": event["fan"]
        }))
