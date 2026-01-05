from django.shortcuts import get_object_or_404

from ..models import ChatGroup
from ..exception import ChatTypeRequired, ChatNameRequired, ChatDoesNotExist, ChatRequired


class ChatService:

    @staticmethod
    def does_chat_exist(chat_name=None):
        if not chat_name:
            return ChatNameRequired("Chat name is required")

        if ChatGroup.objects.filter(chat_name=chat_name).exists():
            return True

        return False

    @staticmethod
    def get_groups(user, chat_type=None):
        if not chat_type:
            return ChatTypeRequired("Chat type is required")

        if chat_type == "global":
            return ChatGroup.objects.filter(chat_type="global")
        elif chat_type == "group":
            return ChatGroup.objects.filter(chat_type="group", members=user)
        elif chat_type == "private":
            return ChatGroup.objects.filter(chat_type="private", members=user).prefetch_related("members")

        return None

    @staticmethod
    def get_chats(chat_type=None, chat_name=None):
        if not chat_type:
            return ChatTypeRequired("Chat type is required")

        if not chat_name:
            return ChatNameRequired("Chat name is required")

        chat = get_object_or_404(
            ChatGroup,
            chat_type=chat_type,
            chat_name=chat_name,
        )

        if not chat:
            return ChatDoesNotExist("Chat does not exist")

        return chat

    @staticmethod
    def get_group_members(chat=None):
        if not chat:
            return ChatRequired("Chat is required")

        return chat.members.value_list("username", flat=True)

    @staticmethod
    def get_other_member(user_id, chat=None):
        if not chat:
            return ChatRequired("Chat is required")

        return chat.members.exclude(id=user_id).first()

    @staticmethod
    def get_chat_messages(chat=None):
        if not chat:
            return ChatRequired("Chat is required")

        return chat.chat_messages.select_related("author").order_by("-created_at")[:60]
