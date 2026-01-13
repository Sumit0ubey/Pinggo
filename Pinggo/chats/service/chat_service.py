from channels.db import database_sync_to_async
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from users.services.user_service import UserService

from ..models import ChatGroup


class ChatService:

    @staticmethod
    def does_chat_exist(chat_name):
        if ChatGroup.objects.filter(group_name=chat_name).exists():
            return True

        return False


    @staticmethod
    async def async_get_chat(chat_name): # DON'T TOUCH IT, IT WORKS WITH CONSUMER
        return await database_sync_to_async(ChatGroup.objects.get)(
            group_name=chat_name
        )


    @staticmethod
    def get_global_chats():
        return ChatGroup.objects.filter(chat_type="global")


    @staticmethod
    def get_group_chats(user):
        return ChatGroup.objects.filter(chat_type="group", members=user)


    @staticmethod
    def get_private_chats(user):
        return ChatGroup.objects.filter(chat_type="private", members=user).prefetch_related("members")


    @staticmethod
    def get_chat_404(chat_type, chat_name):
        return get_object_or_404(
            ChatGroup,
            chat_type=chat_type,
            group_name=chat_name,
        )


    @staticmethod
    def get_chat(chat_type, chat_name):
        return ChatGroup.objects.filter(
            chat_type=chat_type,
            group_name=chat_name,
        ).first()


    @staticmethod
    def is_member(chat, user_id):
        return chat.members.filter(id=user_id).exists()


    @staticmethod
    def get_members(chat):
        return chat.members.all()


    @staticmethod
    def get_members_username(chat):
        return chat.members.values_list("username", flat=True)


    @staticmethod
    def get_other_member(user_id, chat):
        return chat.members.exclude(id=user_id).first()


    @staticmethod
    def get_chat_messages(chat):
        return chat.chat_messages.select_related("author").order_by("-created_at")[:60]


    @staticmethod
    def create_group(user, group_name, description, chat_type, creator, image, members):
        try:
            with transaction.atomic():
                group = ChatGroup.objects.create(
                    group_name=group_name,
                    description=description,
                    chat_type=chat_type,
                    creator=creator,
                )

                if image:
                    group.image_url = image

                group.members.add(user)

                for username in members:
                    try:
                        member_user = UserService.get_user_object_404(username=username)
                        group.members.add(member_user)
                    except User.DoesNotExist:
                        pass

            return True
        except IntegrityError:
            return False


    @staticmethod
    def update_group(group, group_name, description, image, members):
        try:
            with transaction.atomic():

                group.group_name = group_name
                group.description = description

                if image:
                    group.image_url = image

                if group.chat_type == "group":
                    users = list(UserService.get_users_object(members))
                    users.append(group.creator)
                    group.members.set(users)

                group.save()

                return True
        except IntegrityError:
            return False


    @staticmethod
    def get_or_create_private_chat(group_name, current_user, other_user):
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
                return False

            chat.members.add(current_user, other_user)

        return True


    @staticmethod
    def delete_group(chat_type, group_name):
        deleted_count, _ = ChatGroup.objects.filter(chat_type=chat_type, group_name=group_name).delete()
        return deleted_count
