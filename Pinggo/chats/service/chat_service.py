from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from users.services.user_service import UserService

from ..models import ChatGroup
from ..utility import private_room_name


class ChatService:

    @staticmethod
    def does_chat_exist(chat_name):
        if ChatGroup.objects.filter(chat_name=chat_name).exists():
            return True

        return False

    @staticmethod
    def get_groups(user, chat_type):
        if chat_type == "global":
            return ChatGroup.objects.filter(chat_type="global")
        elif chat_type == "group":
            return ChatGroup.objects.filter(chat_type="group", members=user)
        elif chat_type == "private":
            return ChatGroup.objects.filter(chat_type="private", members=user).prefetch_related("members")

        return None

    @staticmethod
    def get_chat(chat_type, chat_name):
        return get_object_or_404(
            ChatGroup,
            chat_type=chat_type,
            chat_name=chat_name,
        )


    @staticmethod
    def get_group_members(chat):
        return chat.members.value_list("username", flat=True)


    @staticmethod
    def get_other_member(user_id, chat):
        return chat.members.exclude(id=user_id).first()


    @staticmethod
    def get_chat_messages(chat):
        return chat.chat_messages.select_related("author").order_by("-created_at")[:60]


    @staticmethod
    def create_group(user, group_name, description, chat_type, creator, image, members):
        if ChatService.does_chat_exist(group_name):
            return JsonResponse({"success": False, "error": "Group already exists"})

        group = ChatGroup.objects.create(
            group_name=group_name,
            description=description,
            chat_type=chat_type,
            creator=creator,
        )

        if image:
            group.image = image
            group.save()

        group.members.add(user)

        for username in members:
            try:
                user = UserService.get_user_object(username=username)
                group.members.add(user)
            except User.DoesNotExist:
                pass

        return JsonResponse({"success": True, "group_name":group_name})


    @staticmethod
    def update_group(chat_type, group_name, description, image, members):
        group = ChatService.get_chat(chat_type, group_name)

        if not group:
            return JsonResponse({"success": False, "error": "Chat does not exist"})

        group.group_name = group_name
        group.description = description

        if image:
            group.image = image

        if group.chat_type == "group":
            users = list(UserService.get_users_object(members))
            users.append(group.creator)
            group.members.set(users)

        group.save()

        return JsonResponse({"success": True, "group_name":group.group_name})


    @staticmethod
    def get_or_create_private_chat(current_user, other_user):
        group_name = private_room_name(current_user, other_user)

        with transaction.atomic():
            chat, created = ChatGroup.objects.get_or_create(
                group_name=group_name,
                chat_type="private",
                defaults={
                    "description": "Private Chat",
                    "creator": current_user,
                }
            )

            if not chat:
                return JsonResponse({"success": False, "error": "Chat does not exist or wasn't created"})

            chat.members.add(other_user, current_user)

        return JsonResponse({"success": True, "group_name":group_name})
