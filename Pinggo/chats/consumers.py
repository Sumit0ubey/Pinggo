from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from channels.db import database_sync_to_async
import json

from .presence import Presence
from .service.chat_service import ChatService
from .service.message_service import MessageService


class ChatroomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.chatroom_type = self.scope["url_route"]["kwargs"]["chatroom_type"]
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]


        self.chatroom = await ChatService.async_get_chat(self.chatroom_name)

        await self.channel_layer.group_add(
            f"{self.chatroom_type}-{self.chatroom_name}",
            self.channel_name
        )

        await self.accept()

        Presence.add(self.chatroom_type ,self.chatroom_name, self.user.id)
        await self.broadcast_online_user_count()


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        body = data["message"]

        message = await MessageService.create_message(
            user=self.user,
            group=self.chatroom,
            message=body,
        )

        await self.channel_layer.group_send(
            f"{self.chatroom_type}-{self.chatroom_name}",
            {
                "type": "message_handler",
                "message_id": message.id,
            }
        )


    async def message_handler(self, event):
        message = await MessageService.get_message(
            message_id=event["message_id"]
        )

        html = await database_sync_to_async(render_to_string)(
            "chats/partials/chat_message_p.html",
            {
                "message": message,
                "user": self.user,
            }
        )

        await self.send(text_data=html)


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"{self.chatroom_type}-{self.chatroom_name}",
            self.channel_name
        )

        Presence.remove(self.chatroom_type, self.chatroom_name, self.user.id)
        await self.broadcast_online_user_count()

    async def broadcast_online_user_count(self):
        count = Presence.count(self.chatroom_type, self.chatroom_name) - 1
        await self.channel_layer.group_send(
            f"{self.chatroom_type}-{self.chatroom_name}",
            {
                "type": "online_count_handler",
                "count": count,
            }
        )

    async def online_count_handler(self, event):
        html = await database_sync_to_async(render_to_string)("chats/partials/online_count.html", {"count": event["count"]})
        await self.send(text_data=html)
