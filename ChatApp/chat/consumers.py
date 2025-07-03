from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from asgiref.sync import sync_to_async
from django.utils import timezone
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self): # работает с экземпляром веб-сокета который был создан   
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.groupName = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.groupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code): # удаляет экземпляр из группы
        await self.channel_layer.group_discard(
            self.groupName,
            self.channel_name
        )

    async def receive(self, text_data): # работает, когда происходит отправка данных через WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        room_obj, _ = await sync_to_async(RoomName.objects.get_or_create)(name=self.room_name)

        await sync_to_async(GroupMessage.objects.create)(
            room_name = room_obj,
            author = user,
            content = message,
            timestamp = timezone.now()
        )

        await self.channel_layer.group_send(
            self.groupName, {
                "type": "sendMessage",
                "message": message,
                "username": user.username,
            }
        )

    async def sendMessage(self, data): # принимает экземпляр, который отправляет данные, и событие
        message = data["message"]
        username = data["username"]
        timestamp = data.get('timestamp'),
        await self.send(text_data=json.dumps({"message": message, "username": username, "timestamp": timestamp}))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): # работает с экземпляром веб-сокета который был создан   
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chatId = f"private_chat_{self.chat_id}"
        await self.channel_layer.group_add(
            self.chatId,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code): # удаляет экземпляр из группы
        await self.channel_layer.group_discard(
            self.chatId,
            self.channel_name
        )

    async def receive(self, text_data): # работает, когда происходит отправка данных через WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        chat_obj, _ = await sync_to_async(PrivateChat.objects.get_or_create)(id=self.chat_id)

        await sync_to_async(PrivateMessage.objects.create)(
            private_chat = chat_obj,
            author = user,
            content = message,
            timestamp = timezone.now()
        )

        await self.channel_layer.group_send(
            self.chatId, {
                "type": "sendMessage",
                "message": message,
                "username": user.username,
            }
        )

    async def sendMessage(self, data): # принимает экземпляр, который отправляет данные, и событие
        message = data["message"]
        username = data["username"]
        timestamp = data.get('timestamp'),
        await self.send(text_data=json.dumps({"message": message, "username": username, "timestamp": timestamp}))
